from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from .models import Vendor, Rider

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Test cases for CustomUser model"""
    
    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'phone_number': '1234567890',
        }
    
    def test_create_user_with_default_type(self):
        """Test creating a user with default user_type"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.user_type, 'user')
        self.assertFalse(user.is_verified)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
    
    def test_create_admin_user(self):
        """Test creating an admin user"""
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            user_type='admin'
        )
        self.assertEqual(user.user_type, 'admin')
    
    def test_create_vendor_user(self):
        """Test creating a vendor user"""
        user = User.objects.create_user(
            username='vendor1',
            email='vendor@example.com',
            password='vendor123',
            user_type='vendor'
        )
        self.assertEqual(user.user_type, 'vendor')
    
    def test_create_rider_user(self):
        """Test creating a rider user"""
        user = User.objects.create_user(
            username='rider1',
            email='rider@example.com',
            password='rider123',
            user_type='rider'
        )
        self.assertEqual(user.user_type, 'rider')
    
    def test_user_phone_number_optional(self):
        """Test that phone_number is optional"""
        user = User.objects.create_user(
            username='nophone',
            email='nophone@example.com',
            password='pass123'
        )
        self.assertIsNone(user.phone_number)
    
    def test_user_profile_picture_optional(self):
        """Test that profile_picture is optional"""
        user = User.objects.create_user(**self.user_data)
        self.assertFalse(user.profile_picture)
    
    def test_user_profile_picture_upload(self):
        """Test uploading a profile picture"""
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_content',
            content_type='image/jpeg'
        )
        user = User.objects.create_user(**self.user_data)
        user.profile_picture = image
        user.save()
        self.assertTrue(user.profile_picture)
    
    def test_user_timestamps(self):
        """Test that created_at and updated_at are set automatically"""
        user = User.objects.create_user(**self.user_data)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
    
    def test_user_verification_default_false(self):
        """Test that is_verified defaults to False"""
        user = User.objects.create_user(**self.user_data)
        self.assertFalse(user.is_verified)
    
    def test_user_verification_can_be_set(self):
        """Test that user can be verified"""
        user = User.objects.create_user(**self.user_data)
        user.is_verified = True
        user.save()
        self.assertTrue(user.is_verified)


class VendorModelTest(TestCase):
    """Test cases for Vendor model"""
    
    def setUp(self):
        """Set up test data"""
        self.vendor_user = User.objects.create_user(
            username='vendoruser',
            email='vendor@test.com',
            password='vendor123',
            user_type='vendor'
        )
        self.vendor_data = {
            'user': self.vendor_user,
            'business_name': 'Test Business',
            'business_address': '123 Test Street',
            'business_phone': '1234567890',
            'business_email': 'business@test.com',
            'business_description': 'A test business',
        }
    
    def test_create_vendor(self):
        """Test creating a vendor"""
        vendor = Vendor.objects.create(**self.vendor_data)
        self.assertEqual(vendor.business_name, 'Test Business')
        self.assertEqual(vendor.user, self.vendor_user)
        self.assertFalse(vendor.is_approved)
    
    def test_vendor_str_representation(self):
        """Test vendor string representation"""
        vendor = Vendor.objects.create(**self.vendor_data)
        self.assertEqual(str(vendor), 'Test Business')
    
    def test_vendor_one_to_one_relationship(self):
        """Test that one user can only have one vendor profile"""
        Vendor.objects.create(**self.vendor_data)
        with self.assertRaises(IntegrityError):
            Vendor.objects.create(**self.vendor_data)
    
    def test_vendor_approval_default_false(self):
        """Test that is_approved defaults to False"""
        vendor = Vendor.objects.create(**self.vendor_data)
        self.assertFalse(vendor.is_approved)
    
    def test_vendor_can_be_approved(self):
        """Test that vendor can be approved"""
        vendor = Vendor.objects.create(**self.vendor_data)
        vendor.is_approved = True
        vendor.save()
        self.assertTrue(vendor.is_approved)
    
    def test_vendor_description_optional(self):
        """Test that business_description is optional"""
        data = self.vendor_data.copy()
        data['business_description'] = ''
        vendor = Vendor.objects.create(**data)
        self.assertEqual(vendor.business_description, '')
    
    def test_vendor_timestamps(self):
        """Test that created_at and updated_at are set"""
        vendor = Vendor.objects.create(**self.vendor_data)
        self.assertIsNotNone(vendor.created_at)
        self.assertIsNotNone(vendor.updated_at)
    
    def test_vendor_cascade_delete(self):
        """Test that vendor is deleted when user is deleted"""
        vendor = Vendor.objects.create(**self.vendor_data)
        vendor_id = vendor.id
        self.vendor_user.delete()
        with self.assertRaises(Vendor.DoesNotExist):
            Vendor.objects.get(id=vendor_id)


class RiderModelTest(TestCase):
    """Test cases for Rider model"""
    
    def setUp(self):
        """Set up test data"""
        self.rider_user = User.objects.create_user(
            username='rideruser',
            email='rider@test.com',
            password='rider123',
            user_type='rider',
            first_name='John',
            last_name='Doe'
        )
        self.rider_data = {
            'user': self.rider_user,
            'phone_number': '9876543210',
            'vehicle_type': 'motorcycle',
            'vehicle_plate': 'ABC123',
        }
    
    def test_create_rider(self):
        """Test creating a rider"""
        rider = Rider.objects.create(**self.rider_data)
        self.assertEqual(rider.phone_number, '9876543210')
        self.assertEqual(rider.vehicle_type, 'motorcycle')
        self.assertEqual(rider.user, self.rider_user)
    
    def test_rider_str_representation(self):
        """Test rider string representation"""
        rider = Rider.objects.create(**self.rider_data)
        expected_str = f'{self.rider_user.get_full_name()} - motorcycle'
        self.assertEqual(str(rider), expected_str)
    
    def test_rider_one_to_one_relationship(self):
        """Test that one user can only have one rider profile"""
        Rider.objects.create(**self.rider_data)
        with self.assertRaises(IntegrityError):
            Rider.objects.create(**self.rider_data)
    
    def test_rider_bicycle_vehicle(self):
        """Test creating rider with bicycle"""
        data = self.rider_data.copy()
        data['vehicle_type'] = 'bicycle'
        rider = Rider.objects.create(**data)
        self.assertEqual(rider.vehicle_type, 'bicycle')
    
    def test_rider_car_vehicle(self):
        """Test creating rider with car"""
        data = self.rider_data.copy()
        data['vehicle_type'] = 'car'
        rider = Rider.objects.create(**data)
        self.assertEqual(rider.vehicle_type, 'car')
    
    def test_rider_availability_default_true(self):
        """Test that is_available defaults to True"""
        rider = Rider.objects.create(**self.rider_data)
        self.assertTrue(rider.is_available)
    
    def test_rider_approval_default_false(self):
        """Test that is_approved defaults to False"""
        rider = Rider.objects.create(**self.rider_data)
        self.assertFalse(rider.is_approved)
    
    def test_rider_can_be_approved(self):
        """Test that rider can be approved"""
        rider = Rider.objects.create(**self.rider_data)
        rider.is_approved = True
        rider.save()
        self.assertTrue(rider.is_approved)
    
    def test_rider_availability_toggle(self):
        """Test toggling rider availability"""
        rider = Rider.objects.create(**self.rider_data)
        rider.is_available = False
        rider.save()
        self.assertFalse(rider.is_available)
    
    def test_rider_vehicle_plate_optional(self):
        """Test that vehicle_plate is optional"""
        data = self.rider_data.copy()
        data['vehicle_plate'] = ''
        rider = Rider.objects.create(**data)
        self.assertEqual(rider.vehicle_plate, '')
    
    def test_rider_created_at(self):
        """Test that created_at is set automatically"""
        rider = Rider.objects.create(**self.rider_data)
        self.assertIsNotNone(rider.created_at)
    
    def test_rider_cascade_delete(self):
        """Test that rider is deleted when user is deleted"""
        rider = Rider.objects.create(**self.rider_data)
        rider_id = rider.id
        self.rider_user.delete()
        with self.assertRaises(Rider.DoesNotExist):
            Rider.objects.get(id=rider_id)


class ModelIntegrationTest(TestCase):
    """Integration tests for multiple models"""
    
    def test_create_complete_vendor_profile(self):
        """Test creating a complete vendor with user"""
        user = User.objects.create_user(
            username='fullvendor',
            email='full@vendor.com',
            password='pass123',
            user_type='vendor',
            phone_number='1112223333',
            is_verified=True
        )
        vendor = Vendor.objects.create(
            user=user,
            business_name='Full Business',
            business_address='456 Business Ave',
            business_phone='4445556666',
            business_email='full@business.com',
            business_description='Complete business',
            is_approved=True
        )
        
        self.assertEqual(vendor.user.user_type, 'vendor')
        self.assertTrue(vendor.user.is_verified)
        self.assertTrue(vendor.is_approved)
    
    def test_create_complete_rider_profile(self):
        """Test creating a complete rider with user"""
        user = User.objects.create_user(
            username='fullrider',
            email='full@rider.com',
            password='pass123',
            user_type='rider',
            phone_number='7778889999',
            first_name='Jane',
            last_name='Smith'
        )
        rider = Rider.objects.create(
            user=user,
            phone_number='7778889999',
            vehicle_type='car',
            vehicle_plate='XYZ789',
            is_approved=True,
            is_available=True
        )
        
        self.assertEqual(rider.user.user_type, 'rider')
        self.assertTrue(rider.is_approved)
        self.assertTrue(rider.is_available)
        self.assertIn('Jane Smith', str(rider))
        