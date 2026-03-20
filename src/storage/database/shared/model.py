from coze_coding_dev_sdk.database import Base

from typing import Optional
import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, ForeignKeyConstraint, Integer, JSON, Numeric, PrimaryKeyConstraint, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import Mapped, mapped_column, relationship

class HealthCheck(Base):
    __tablename__ = 'health_check'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='health_check_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))


class PetTypes(Base):
    __tablename__ = 'pet_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pet_types_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment='宠物名称')
    description: Mapped[str] = mapped_column(Text, nullable=False, comment='宠物描述')
    element: Mapped[str] = mapped_column(String(50), nullable=False, comment='元素属性(金木水火土)')
    rarity: Mapped[str] = mapped_column(String(20), nullable=False, comment='稀有度(普通/稀有/史诗/传说)')
    base_image_url: Mapped[str] = mapped_column(String(500), nullable=False, comment='基础形象图片URL')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    pet_skills: Mapped[list['PetSkills']] = relationship('PetSkills', back_populates='pet_type')
    pet_stages: Mapped[list['PetStages']] = relationship('PetStages', back_populates='pet_type')
    user_pets: Mapped[list['UserPets']] = relationship('UserPets', back_populates='pet_type')


t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('shared_blk_read_time', Double(53)),
    Column('shared_blk_write_time', Double(53)),
    Column('local_blk_read_time', Double(53)),
    Column('local_blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53)),
    Column('jit_deform_count', BigInteger),
    Column('jit_deform_time', Double(53)),
    Column('stats_since', DateTime(True)),
    Column('minmax_stats_since', DateTime(True))
)


t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('username', name='users_username_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, comment='用户名')
    email: Mapped[str] = mapped_column(String(100), nullable=False, comment='邮箱')
    display_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='显示名称')
    total_points: Mapped[int] = mapped_column(Integer, nullable=False, comment='总积分')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), comment='头像URL')
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    user_pets: Mapped[list['UserPets']] = relationship('UserPets', back_populates='user')
    point_records: Mapped[list['PointRecords']] = relationship('PointRecords', back_populates='user')


class PetSkills(Base):
    __tablename__ = 'pet_skills'
    __table_args__ = (
        ForeignKeyConstraint(['pet_type_id'], ['pet_types.id'], name='pet_skills_pet_type_id_fkey'),
        PrimaryKeyConstraint('id', name='pet_skills_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_type_id: Mapped[int] = mapped_column(Integer, nullable=False, comment='宠物类型ID')
    stage_level: Mapped[int] = mapped_column(Integer, nullable=False, comment='解锁阶段等级')
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='技能名称')
    skill_type: Mapped[str] = mapped_column(String(50), nullable=False, comment='技能类型(特效/被动/主动)')
    effect_description: Mapped[str] = mapped_column(Text, nullable=False, comment='效果描述')
    effect_config: Mapped[dict] = mapped_column(JSON, nullable=False, comment='效果配置')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    pet_type: Mapped['PetTypes'] = relationship('PetTypes', back_populates='pet_skills')


class PetStages(Base):
    __tablename__ = 'pet_stages'
    __table_args__ = (
        ForeignKeyConstraint(['pet_type_id'], ['pet_types.id'], name='pet_stages_pet_type_id_fkey'),
        PrimaryKeyConstraint('id', name='pet_stages_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_type_id: Mapped[int] = mapped_column(Integer, nullable=False, comment='宠物类型ID')
    stage_level: Mapped[int] = mapped_column(Integer, nullable=False, comment='阶段等级(1-4)')
    stage_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='阶段名称')
    required_points: Mapped[int] = mapped_column(Integer, nullable=False, comment='解锁所需积分')
    image_url: Mapped[str] = mapped_column(String(500), nullable=False, comment='该阶段形象URL')
    description: Mapped[str] = mapped_column(Text, nullable=False, comment='阶段描述')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    pet_type: Mapped['PetTypes'] = relationship('PetTypes', back_populates='pet_stages')


class UserPets(Base):
    __tablename__ = 'user_pets'
    __table_args__ = (
        ForeignKeyConstraint(['pet_type_id'], ['pet_types.id'], name='user_pets_pet_type_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='user_pets_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_pets_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment='用户ID')
    pet_type_id: Mapped[int] = mapped_column(Integer, nullable=False, comment='宠物类型ID')
    current_stage: Mapped[int] = mapped_column(Integer, nullable=False, comment='当前阶段')
    total_points: Mapped[int] = mapped_column(Integer, nullable=False, comment='累计积分')
    unlocked_stages: Mapped[dict] = mapped_column(JSON, nullable=False, comment='已解锁阶段')
    unlocked_skills: Mapped[dict] = mapped_column(JSON, nullable=False, comment='已解锁技能')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    nickname: Mapped[Optional[str]] = mapped_column(String(100), comment='宠物昵称')
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    pet_type: Mapped['PetTypes'] = relationship('PetTypes', back_populates='user_pets')
    user: Mapped['Users'] = relationship('Users', back_populates='user_pets')
    point_records: Mapped[list['PointRecords']] = relationship('PointRecords', back_populates='user_pet')


class PointRecords(Base):
    __tablename__ = 'point_records'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='point_records_user_id_fkey'),
        ForeignKeyConstraint(['user_pet_id'], ['user_pets.id'], name='point_records_user_pet_id_fkey'),
        PrimaryKeyConstraint('id', name='point_records_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment='用户ID')
    points: Mapped[int] = mapped_column(Integer, nullable=False, comment='积分变动(正数增加,负数减少)')
    reason: Mapped[str] = mapped_column(String(200), nullable=False, comment='积分原因')
    category: Mapped[str] = mapped_column(String(50), nullable=False, comment='积分类别(作业/表现/奖励等)')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    user_pet_id: Mapped[Optional[int]] = mapped_column(Integer, comment='关联宠物ID')

    user: Mapped['Users'] = relationship('Users', back_populates='point_records')
    user_pet: Mapped[Optional['UserPets']] = relationship('UserPets', back_populates='point_records')
