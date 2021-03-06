#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import *
from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()

class ReprMixin(object):
    """Hooks into SQLAlchemy's magic to make :meth:`__repr__`s.
    Source from: http://innuendopoly.org/arch/sqlalchemy-init-repr

    Any class that uses this mixin will have reprs in this format:
    Class(<col name>=<col value>,..)
    For all columns
    """
    def __repr__(self):
        def reprs():
            for col in self.__table__.c:
                yield col.name, repr(getattr(self, col.name))

        def format(seq):
            for key, value in seq:
                yield '%s=%s' % (key, value)

        args = '(%s)' % ', '.join(format(reprs()))
        classy = type(self).__name__
        return classy + args

class DevRankMixin(object):

    def columns(self):
        for col in self.__table__.c:
            yield col.name

    def from_dict(self, obj_dict):
        for col in self.columns():
            if col in obj_dict:
                setattr(self, col, obj_dict[col])
        return self

class User(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(45))
    name = Column(String(45))
    etag = Column(String(45))
    gravatar_id = Column(String(45))
    avatar_url = Column(String(200))
    blog = Column(String(200))
    location = Column(String(45))
    email = Column(String(45))
    bio = Column(String(45))
    company = Column(String(45))
    hireable = Column(Boolean)
    crawled_at = Column(DateTime)
    devrank_score = Column(Float(30))

    def __init__(self):
        self.devrank_score = 0.0
        pass

    def followers(self):
        #TODO
        pass

    def friends(self, depth=1):
        #TODO
        pass

    def orgs(self):
        #TODO
        pass


class Follower(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'followings'

    src_id = Column(Integer, primary_key=True)
    dest_id = Column(Integer, primary_key=True)

    def __init__(self, src_id, dest_id):
        self.src_id = src_id
        self.dest_id = dest_id


class Friendship(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'friendship'

    owner_id = Column(Integer, primary_key=True)
    friend_id = Column(Integer, primary_key=True)

    def __init__(self, owner_id, friend_id):
        self.owner_id = owner_id
        self.friend_id = friend_id

class Repo(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'repos'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    name = Column(String(45))
    description = Column(Text)
    fork = Column(Boolean)
    fork_owner_id = Column(Integer)
    language = Column(String(45))
    etag = Column(String(45))
    crawled_at = Column(DateTime)

    def __init__(self):
        pass

    def watchers(self):
        #TODO
        pass

    def stargazers(self):
        #TODO
        pass

    def contributors(self):
        #TODO
        pass

class Watcher(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'watchers'

    watcher_id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, primary_key=True)

    def __init__(self, watcher_id, repo_id):
        self.watcher_id = watcher_id
        self.repo_id = repo_id

class Stargazer(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'stargazers'

    stargazer_id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, primary_key=True)

    def __init__(self, stargazer_id, repo_id):
        self.stargazer_id = stargazer_id
        self.repo_id = repo_id

class Contributor(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'contributors'

    repo_id = Column(Integer, primary_key=True)
    contributor_id = Column(Integer, primary_key=True)
    contributions = Column(Integer)

    def __init__(self, repo_id, contributor_id, contributions):
        self.repo_id = repo_id
        self.contributor_id = contributor_id
        self.contributions = contributions

class Org(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'orgs'

    org_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, primary_key=True)

    def __init__(self, org_id, member_id):
        self.org_id = org_id
        self.member_id = member_id

    def members(self):
        #TODO
        pass

class Member(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'members'

    login = Column(String(45), primary_key=True)

    def __init__(self, login):
        self.login = login

class TaskQueue(ReprMixin, DevRankMixin, Base):
    __tablename__ = 'queue'

    task_id = Column(Integer, primary_key=True)
    login = Column(String(45))
    user_id = Column(Integer)
    reponame = Column(String(45))
    repo_id = Column(Integer)
    root_login = Column(String(45))
    task_type = Column(Integer)
    method = Column(String(50))
    assignee = Column(String(150))
    assigned_dt = Column(DateTime)
    completed_dt = Column(DateTime)
    success = Column(Boolean)
    __table_args__ = (
        UniqueConstraint('login', 'method', name='_queue_login_method_uc'),
    )

    def __init__(self):
        pass
