import unittest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from domain.entities.member import Member, MemberType, MemberStatus


class TestMemberEntity(unittest.TestCase):
    """Test cases cho Member entity"""
    
    def setUp(self):
        """Setup test data"""
        self.member = Member(
            member_code="DV001",
            full_name="Nguyễn Văn A",
            member_type=MemberType.UNION_MEMBER,
            status=MemberStatus.ACTIVE
        )
    
    def test_member_creation(self):
        """Test tạo member"""
        self.assertEqual(self.member.member_code, "DV001")
        self.assertEqual(self.member.full_name, "Nguyễn Văn A")
        self.assertEqual(self.member.member_type, MemberType.UNION_MEMBER)
        self.assertEqual(self.member.status, MemberStatus.ACTIVE)
        self.assertIsNotNone(self.member.created_at)
    
    def test_is_active(self):
        """Test kiểm tra trạng thái active"""
        self.assertTrue(self.member.is_active())
        
        self.member.status = MemberStatus.INACTIVE
        self.assertFalse(self.member.is_active())
    
    def test_get_display_name(self):
        """Test lấy tên hiển thị"""
        display_name = self.member.get_display_name()
        self.assertEqual(display_name, "DV001 - Nguyễn Văn A")


if __name__ == '__main__':
    unittest.main()