from coze_coding_dev_sdk.database import Base

from typing import Optional
import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, Integer, Numeric, PrimaryKeyConstraint, Table, Text, text, String, ForeignKey, JSON, func
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import Mapped, mapped_column

class HealthCheck(Base):
    __tablename__ = 'health_check'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='health_check_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))


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


# ========== 业务表定义 ==========

class User(Base):
    """用户表"""
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, comment="邮箱")
    display_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="显示名称")
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="头像URL")
    total_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="总积分")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class PetType(Base):
    """宠物类型表 - 山海经生物种类"""
    __tablename__ = 'pet_types'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="宠物名称")
    description: Mapped[str] = mapped_column(Text, nullable=False, comment="宠物描述")
    element: Mapped[str] = mapped_column(String(50), nullable=False, comment="元素属性(金木水火土)")
    rarity: Mapped[str] = mapped_column(String(20), nullable=False, comment="稀有度(普通/稀有/史诗/传说)")
    base_image_url: Mapped[str] = mapped_column(String(500), nullable=False, comment="基础形象图片URL")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PetStage(Base):
    """宠物进化阶段表"""
    __tablename__ = 'pet_stages'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('pet_types.id'), nullable=False, comment="宠物类型ID")
    stage_level: Mapped[int] = mapped_column(Integer, nullable=False, comment="阶段等级(1-4)")
    stage_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="阶段名称")
    required_points: Mapped[int] = mapped_column(Integer, nullable=False, comment="解锁所需积分")
    image_url: Mapped[str] = mapped_column(String(500), nullable=False, comment="该阶段形象URL")
    description: Mapped[str] = mapped_column(Text, nullable=False, comment="阶段描述")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class UserPet(Base):
    """用户宠物表"""
    __tablename__ = 'user_pets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, comment="用户ID")
    pet_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('pet_types.id'), nullable=False, comment="宠物类型ID")
    nickname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="宠物昵称")
    current_stage: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="当前阶段")
    total_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="累计积分")
    unlocked_stages: Mapped[dict] = mapped_column(JSON, default={}, nullable=False, comment="已解锁阶段")
    unlocked_skills: Mapped[dict] = mapped_column(JSON, default={}, nullable=False, comment="已解锁技能")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class PetSkill(Base):
    """宠物技能表"""
    __tablename__ = 'pet_skills'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('pet_types.id'), nullable=False, comment="宠物类型ID")
    stage_level: Mapped[int] = mapped_column(Integer, nullable=False, comment="解锁阶段等级")
    skill_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="技能名称")
    skill_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="技能类型(特效/被动/主动)")
    effect_description: Mapped[str] = mapped_column(Text, nullable=False, comment="效果描述")
    effect_config: Mapped[dict] = mapped_column(JSON, default={}, nullable=False, comment="效果配置")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PointRecord(Base):
    """积分记录表"""
    __tablename__ = 'point_records'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, comment="用户ID")
    user_pet_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('user_pets.id'), nullable=True, comment="关联宠物ID")
    points: Mapped[int] = mapped_column(Integer, nullable=False, comment="积分变动(正数增加,负数减少)")
    reason: Mapped[str] = mapped_column(String(200), nullable=False, comment="积分原因")
    category: Mapped[str] = mapped_column(String(50), nullable=False, comment="积分类别(作业/表现/奖励等)")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
