__all__ = [
    "GitHubWebhookService"
]

from logging import getLogger
from typing import Type

from sqlalchemy.orm import Session

from validators import GitHubWebhook, Issue, Label, Repository, User
from models import UserORM, RepositoryORM, IssueORM, LabelORM, ReactionsORM

log = getLogger(__name__)


class GitHubWebhookService:
    def __init__(self, db: Session):
        self.db = db

    def handle(self, payload: GitHubWebhook) -> dict:
        try:
            owner = self.upsert_user(payload.repository.owner)
            sender = self.upsert_user(payload.sender)
            issue_user = self.upsert_user(payload.issue.user)

            repo = self.upsert_repository(payload.repository, owner.id)
            issue = self.upsert_issue(payload.issue, issue_user.id)

            issue.labels.clear()
            for label_data in payload.issue.labels:
                label = self.upsert_label(label_data)
                issue.labels.append(label)

            issue.assignees.clear()
            assignees = payload.issue.assignees
            if assignee := payload.issue.assignee:
                assignees.append(assignee)

            for assignee_data in assignees:
                assignee = self.upsert_user(assignee_data)
                issue.assignees.append(assignee)

            existing = self.db.query(ReactionsORM).filter_by(issue_id=issue.id).all()
            for r in existing:
                self.db.delete(r)
                self.db.flush()

            self.db.add(ReactionsORM(issue_id=issue.id, **payload.issue.reactions.model_dump(mode="json")))

            self.db.commit()

            return {
                "repository": {
                    "id": repo.id,
                    "full_name": repo.full_name,
                    "owner_id": repo.owner_id
                },
                "issue": {
                    "id": issue.id,
                    "number": issue.number,
                    "title": issue.title,
                    "user_id": issue.user_id,
                    "assignee_ids": sorted([u.id for u in issue.assignees]),
                    "label_ids": sorted([l.id for l in issue.labels])
                },
                "sender_id": sender.id
            }
        except Exception as e:
            self.db.rollback()
            log.error("Webhook DB error: %s (%s)", e.__class__.__name__, str(e), exc_info=True)
            raise

    def upsert_user(self, user_data: User) -> Type[UserORM] | UserORM:
        user_dict = user_data.model_dump(mode="json")

        # Look for existing user by GitHub ID (source of truth)
        existing_user = self.db.query(UserORM).filter_by(id=user_dict["id"]).first()
        if existing_user:
            # If login changed (e.g., a user renamed GitHub account), log and update it
            if existing_user.login != user_dict["login"]:
                log.warning(f"[User Update] GitHub login changed: {existing_user.login} → {user_dict['login']}")
                existing_user.login = user_dict["login"]

            # Update all other fields except ID (login already handled)
            for field, value in user_dict.items():
                if field != "id":
                    setattr(existing_user, field, value)

            return existing_user

        # If a user with the same login exists but with a different ID, it's a conflict
        login_conflict = self.db.query(UserORM).filter_by(login=user_dict["login"]).first()
        if login_conflict:
            log.warning(
                f"[User Conflict] Login '{user_dict['login']}' already exists for user ID {login_conflict.id}, "
                f"but received different ID {user_dict['id']} — skipping creation"
            )
            return login_conflict

        # No conflicts — create a brand-new user
        new_user = UserORM(**user_dict)
        self.db.add(new_user)
        self.db.flush()
        return new_user

    def upsert_repository(self, repo_data: Repository, owner_id: int) -> Type[RepositoryORM] | RepositoryORM:
        repo_dict = repo_data.model_dump(mode="json", exclude={"owner"})
        repo_dict["owner_id"] = owner_id

        existing = self.db.query(RepositoryORM).filter_by(id=repo_data.id).first()
        if existing:
            if existing.owner_id != owner_id:
                log.warning(f"[Repository Conflict] Repo ID {repo_data.id} has owner_id={existing.owner_id}, "
                            f"not {owner_id} — skipping ownership update")
            for field, value in repo_dict.items():
                if field != "owner_id":
                    setattr(existing, field, value)
            return existing

        new_repo = RepositoryORM(**repo_dict)
        self.db.add(new_repo)
        self.db.flush()
        return new_repo

    def upsert_issue(self, issue_data: Issue, user_id: int) -> Type[IssueORM] | IssueORM:
        issue_dict = issue_data.model_dump(mode="json", exclude={"user", "assignee", "assignees", "labels", "reactions"})
        issue_dict["user_id"] = user_id

        existing = self.db.query(IssueORM).filter_by(id=issue_data.id).first()
        if existing:
            for field, value in issue_dict.items():
                setattr(existing, field, value)
            return existing

        new_issue = IssueORM(**issue_dict)
        self.db.add(new_issue)
        self.db.flush()
        return new_issue

    def upsert_label(self, label_data: Label) -> Type[LabelORM] | LabelORM:
        existing = self.db.query(LabelORM).filter_by(id=label_data.id).first()
        if existing:
            for field, value in label_data.model_dump(mode="json").items():
                setattr(existing, field, value)
            return existing

        new_label = LabelORM(**label_data.model_dump(mode="json"))
        self.db.add(new_label)
        self.db.flush()
        return new_label
