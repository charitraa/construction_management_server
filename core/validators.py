"""
File upload validators for gallery application.
Provides comprehensive validation for image uploads including type, size, and content checks.
"""

import os
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.conf import settings
from PIL import Image as PILImage
import io


class FileValidator:
    """
    Comprehensive file validator that checks file type, size, and content.
    """

    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
    ALLOWED_MIME_TYPES = [
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/gif',
        'image/webp',
        'image/bmp'
    ]

    # File size limits (in bytes)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MIN_FILE_SIZE = 100  # 100 bytes minimum (for small test images)

    # Image dimensions limits
    MAX_WIDTH = 10000  # pixels
    MAX_HEIGHT = 10000  # pixels
    MIN_WIDTH = 1  # pixel
    MIN_HEIGHT = 1  # pixel

    def __call__(self, file):
        """
        Validate the uploaded file.

        Args:
            file: The uploaded file object

        Raises:
            ValidationError: If validation fails
        """
        # Reset file pointer
        file.seek(0)

        # Check file size
        self._validate_file_size(file)

        # Check file extension
        self._validate_file_extension(file)

        # Check MIME type
        self._validate_mime_type(file)

        # Validate that it's actually an image
        self._validate_image_content(file)

        # Check image dimensions
        self._validate_image_dimensions(file)

        # Reset file pointer for further processing
        file.seek(0)

    def _validate_file_size(self, file):
        """Validate file size is within acceptable limits."""
        try:
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > self.MAX_FILE_SIZE:
                raise ValidationError(
                    f'File size {self._format_size(file_size)} exceeds maximum allowed size of {self._format_size(self.MAX_FILE_SIZE)}.'
                )

            if file_size < self.MIN_FILE_SIZE:
                raise ValidationError(
                    f'File size is too small. Minimum size is {self._format_size(self.MIN_FILE_SIZE)}.'
                )
        except (IOError, OSError) as e:
            raise ValidationError(f'Unable to read file size: {str(e)}')

    def _validate_file_extension(self, file):
        """Validate file extension is allowed."""
        filename = file.name.lower()
        if not filename:
            raise ValidationError('File has no name.')

        # Get extension without the dot
        extension = filename.split('.')[-1] if '.' in filename else ''

        if extension not in self.ALLOWED_EXTENSIONS:
            allowed = ', '.join(self.ALLOWED_EXTENSIONS)
            raise ValidationError(
                f'File extension ".{extension}" is not allowed. '
                f'Allowed extensions are: {allowed}.'
            )

    def _validate_mime_type(self, file):
        """Validate file MIME type is allowed."""
        try:
            # Read first few bytes to detect content type
            file.seek(0)
            header = file.read(32)
            file.seek(0)

            # Simple MIME type detection based on file signature
            mime_type = self._detect_mime_type(header)

            if mime_type not in self.ALLOWED_MIME_TYPES:
                allowed = ', '.join(self.ALLOWED_MIME_TYPES)
                raise ValidationError(
                    f'File content type "{mime_type}" is not allowed. '
                    f'Allowed types are: {allowed}.'
                )
        except Exception as e:
            raise ValidationError(f'Unable to validate file content type: {str(e)}')

    def _detect_mime_type(self, header):
        """
        Detect MIME type from file header bytes.
        This is more reliable than checking file extensions.
        """
        if not header:
            return 'application/octet-stream'

        # JPEG: FF D8 FF
        if header[:3] == b'\xff\xd8\xff':
            return 'image/jpeg'

        # PNG: 89 50 4E 47 0D 0A 1A 0A
        if header[:8] == b'\x89PNG\r\n\x1a\n':
            return 'image/png'

        # GIF: 47 49 46 38
        if header[:4] in (b'GIF8', b'GIF7'):
            return 'image/gif'

        # WebP: 52 49 46 46 ... 57 45 42 50
        if len(header) >= 12 and header[:4] == b'RIFF' and header[8:12] == b'WEBP':
            return 'image/webp'

        # BMP: 42 4D
        if header[:2] == b'BM':
            return 'image/bmp'

        # Default to octet-stream if unknown
        return 'application/octet-stream'

    def _validate_image_content(self, file):
        """
        Validate that the file is actually a valid image.
        Uses PIL to attempt to open the file.
        """
        try:
            file.seek(0)
            with PILImage.open(io.BytesIO(file.read())) as img:
                # Verify the image can be loaded
                img.verify()
        except Exception as e:
            raise ValidationError(
                f'File is not a valid image or is corrupted. '
                f'Error: {str(e)}'
            )

    def _validate_image_dimensions(self, file):
        """Validate image dimensions are within acceptable limits."""
        try:
            file.seek(0)
            width, height = get_image_dimensions(file)
            file.seek(0)

            if width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
                raise ValidationError(
                    f'Image dimensions {width}x{height} are too small. '
                    f'Minimum dimensions are {self.MIN_WIDTH}x{self.MIN_HEIGHT}.'
                )

            if width > self.MAX_WIDTH or height > self.MAX_HEIGHT:
                raise ValidationError(
                    f'Image dimensions {width}x{height} exceed maximum allowed size. '
                    f'Maximum dimensions are {self.MAX_WIDTH}x{self.MAX_HEIGHT}.'
                )
        except Exception as e:
            raise ValidationError(f'Unable to validate image dimensions: {str(e)}')

    def _format_size(self, size_bytes):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"


def validate_image_upload(file):
    """
    Convenience function to validate image uploads.
    Can be used in model field validators or serializers.
    """
    validator = FileValidator()
    validator(file)
    return file


class ThumbnailValidator(FileValidator):
    """
    Specific validator for thumbnail uploads.
    Smaller size limits and more restrictive dimensions.
    """

    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB for thumbnails
    MIN_FILE_SIZE = 100  # 100 bytes minimum (for small test images)

    # Thumbnail dimensions should be reasonable
    MAX_WIDTH = 4000  # pixels
    MAX_HEIGHT = 4000  # pixels
    MIN_WIDTH = 50  # pixels
    MIN_HEIGHT = 50  # pixels


def validate_thumbnail_upload(file):
    """
    Convenience function to validate thumbnail uploads.
    """
    validator = ThumbnailValidator()
    validator(file)
    return file
