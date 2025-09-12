from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from domain.entities.member import Member, MemberType, MemberStatus
from domain.repositories.member_repository import IMemberRepository
from infrastructure.database.models import MemberModel
from infrastructure.database.connection import db_manager


class MemberRepository(IMemberRepository):
    """Implementation của Member Repository"""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def _model_to_entity(self, model: MemberModel) -> Member:
        """Chuyển đổi từ SQLAlchemy model sang Domain entity"""
        return Member(
            id=model.id,
            member_code=model.member_code,
            full_name=model.full_name,
            date_of_birth=model.date_of_birth,
            gender=model.gender,
            phone=model.phone,
            email=model.email,
            address=model.address,
            position=model.position,
            department=model.department,
            member_type=model.member_type,
            status=model.status,
            join_date=model.join_date,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: Member) -> MemberModel:
        """Chuyển đổi từ Domain entity sang SQLAlchemy model"""
        return MemberModel(
            id=entity.id,
            member_code=entity.member_code,
            full_name=entity.full_name,
            date_of_birth=entity.date_of_birth,
            gender=entity.gender,
            phone=entity.phone,
            email=entity.email,
            address=entity.address,
            position=entity.position,
            department=entity.department,
            member_type=entity.member_type,
            status=entity.status,
            join_date=entity.join_date,
            notes=entity.notes,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    def create(self, member: Member) -> Member:
        """Tạo thành viên mới"""
        session: Session = self.db_manager.get_session()
        try:
            model = self._entity_to_model(member)
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_by_id(self, member_id: int) -> Optional[Member]:
        """Lấy thành viên theo ID"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(MemberModel).filter(MemberModel.id == member_id).first()
            return self._model_to_entity(model) if model else None
        finally:
            session.close()
    
    def get_by_member_code(self, member_code: str) -> Optional[Member]:
        """Lấy thành viên theo mã thành viên"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(MemberModel).filter(MemberModel.member_code == member_code).first()
            return self._model_to_entity(model) if model else None
        finally:
            session.close()
    
    def get_all(self) -> List[Member]:
        """Lấy tất cả thành viên"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(MemberModel).order_by(MemberModel.full_name).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_type(self, member_type: MemberType) -> List[Member]:
        """Lấy thành viên theo loại"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(MemberModel).filter(
                MemberModel.member_type == member_type
            ).order_by(MemberModel.full_name).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_status(self, status: MemberStatus) -> List[Member]:
        """Lấy thành viên theo trạng thái"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(MemberModel).filter(
                MemberModel.status == status
            ).order_by(MemberModel.full_name).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def search_by_name(self, name: str) -> List[Member]:
        """Tìm kiếm thành viên theo tên"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(MemberModel).filter(
                MemberModel.full_name.contains(name)
            ).order_by(MemberModel.full_name).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def update(self, member: Member) -> Member:
        """Cập nhật thông tin thành viên"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(MemberModel).filter(MemberModel.id == member.id).first()
            if not model:
                raise ValueError(f"Member with ID {member.id} not found")
            
            # Cập nhật các thuộc tính
            model.member_code = member.member_code
            model.full_name = member.full_name
            model.date_of_birth = member.date_of_birth
            model.gender = member.gender
            model.phone = member.phone
            model.email = member.email
            model.address = member.address
            model.position = member.position
            model.department = member.department
            model.member_type = member.member_type
            model.status = member.status
            model.join_date = member.join_date
            model.notes = member.notes
            model.updated_at = member.updated_at
            
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self, member_id: int) -> bool:
        """Xóa thành viên"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(MemberModel).filter(MemberModel.id == member_id).first()
            if not model:
                return False
            
            session.delete(model)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def count_by_type(self, member_type: MemberType) -> int:
        """Đếm số thành viên theo loại"""
        session: Session = self.db_manager.get_session()
        try:
            count = session.query(func.count(MemberModel.id)).filter(
                MemberModel.member_type == member_type
            ).scalar()
            return count or 0
        finally:
            session.close()