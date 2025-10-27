from django.core.validators import RegexValidator

rfc_validador = RegexValidator(
    regex=r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$',
    message='El R.F.C. no tiene un formato valido',
    code='rfc_invalido'
)

curp_validador = RegexValidator(
    regex=r'^[A-ZÑ]{4}\d{6}[HM][A-ZÑ]{5}\d{2}$',
    message='El CURP no tiene un formato valido',
    code='curp_invalido'
)
