from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize= value.size

    if filesize > 20971520:
        raise ValidationError("Możesz dodać plik o maksymalnym rozmiarze 20MB")
    else:
        return value

            
