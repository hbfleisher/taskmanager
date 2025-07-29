import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Setting(Base):
    __tablename__ = 'Setting'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    value_type = Column(String(50), nullable=False)  # e.g., 'string', 'integer', 'boolean'
    value = Column(String(1024), nullable=False)
    description = Column(String(1024), nullable=True)
    created = Column(DateTime, default=func.now())
    modified = Column(DateTime, default=func.now(), onupdate=func.now())
    is_default = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Setting(id={self.id}, name='{self.name}', value='{self.value}', is_default={self.is_default})>"


class Task(Base):
    __tablename__ = 'Task'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    status = Column(String(50), default='pending')  # e.g., 'pending', 'in-progress', 'completed'
    completed = Column(DateTime, default=None, nullable=True)
    created = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', completed={self.completed})>"
    

class TaskSchedule(Base):
    __tablename__ = 'TaskSchedule'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('Task.id'), nullable=False)
    schedule_datetime = Column(DateTime, nullable=False)
    reschedules = Column(Integer, default=0)
    
    task = relationship("Task", back_populates="schedules")
    
    def __repr__(self):
        return f"<TaskSchedule(id={self.id}, task_id={self.task_id}, schedule_datetime={self.schedule_datetime})>"

class TaskScheduleRecurrance(Base):
    __tablename__ = 'TaskScheduleRecurrance'
    
    id = Column(Integer, primary_key=True)
    task_schedule_id = Column(Integer, ForeignKey('TaskSchedule.id'), nullable=False)
    recurrance_type = Column(String(50), nullable=False)  # e.g., 'daily', 'weekly', 'monthly'
    interval = Column(Integer, default=1)  # e.g., every 1 day, every 2 weeks
    
    task_schedule = relationship("TaskSchedule", back_populates="recurrances")
    
    def __repr__(self):
        return f"<TaskScheduleRecurrance(id={self.id}, task_schedule_id={self.task_schedule_id}, recurrance_type='{self.recurrance_type}', interval={self.interval})>"

class TaskStep(Base):
    __tablename__ = 'TaskStep'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('Task.id'), nullable=False)
    subtask_id = Column(Integer, ForeignKey('Task.id'), nullable=True)
    step_description = Column(String(1024), nullable=False)
    step_order = Column(Integer, nullable=False)
    completed = Column(Boolean, default=False)
    
    task = relationship("Task", back_populates="steps")
    subtask = relationship("Task", remote_side=[Task.id], back_populates="subtasks")

    def __repr__(self):
        return f"<TaskStep(id={self.id}, task_id={self.task_id}, step_order={self.step_order}, completed={self.completed})>"

class BingoBoard(Base):
    __tablename__ = 'BingoBoard'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<BingoBoard(id={self.id}, name='{self.name}')>"
    
class BingoBoardTask(Base):
    __tablename__ = 'BingoBoardTask'
    
    id = Column(Integer, primary_key=True)
    bingo_board_id = Column(Integer, ForeignKey('BingoBoard.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('Task.id'), nullable=False)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    
    bingo_board = relationship("BingoBoard", back_populates="tasks")
    task = relationship("Task")
    
    def __repr__(self):
        return f"<BingoBoardTask(id={self.id}, bingo_board_id={self.bingo_board_id}, task_id={self.task_id}, position=({self.position_x}, {self.position_y}))>"
    
class TaskTimer(Base):
    __tablename__ = 'TaskTimer'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    timer_type = Column(String(50), nullable=False)  # e.g., 'abstract', 'concrete'
    task_id = Column(Integer, ForeignKey('Task.id'), nullable=True)
    uses = Column(Integer, default=0)
    
    task = relationship("Task", back_populates="timers")
    
    def __repr__(self):
        return f"<TaskTimer(id={self.id}, task_id={self.task_id}, duration={self.duration}, uses={self.uses})>"
    
class TaskTimerSegment(Base):
    __tablename__ = 'TaskTimerSegment'
    
    id = Column(Integer, primary_key=True)
    task_timer_id = Column(Integer, ForeignKey('TaskTimer.id'), nullable=False)
    segment_order = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=True)  # in seconds
    name = Column(String(255), nullable=True)
    description = Column(String(1024), nullable=True)
    segment_type = Column(String(50), nullable=False)  # e.g., 'countdown', 'stopwatch'
    extra_time = Column(Integer, default=0)  # in seconds
    
    task_timer = relationship("TaskTimer", back_populates="segments")
    
    def __repr__(self):
        return f"<TaskTimerSegment(id={self.id}, task_timer_id={self.task_timer_id}, segment_order={self.segment_order}, segment_duration={self.segment_duration})>"

class TaskTimerSchedule(Base):
    __tablename__ = 'TaskTimerSchedule'
    
    id = Column(Integer, primary_key=True)
    task_timer_id = Column(Integer, ForeignKey('TaskTimer.id'), nullable=False)
    schedule_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    total_time = Column(Integer, nullable=True)  # in seconds
    remaining_time = Column(Integer, nullable=True)  # in seconds
    
    task_timer = relationship("TaskTimer", back_populates="schedules")
    
    def __repr__(self):
        return f"<TaskTimerSchedule(id={self.id}, task_timer_id={self.task_timer_id}, schedule_time={self.schedule_time}, is_active={self.is_active})>"