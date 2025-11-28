from django.core.validators import RegexValidator

ine_validador = RegexValidator(
    regex=r'[BCDFGHJKLMNPQRSTVWXYZ]{6}[0-9]{2}[0-1]{1}[0-9]{1}[0-3]{1}[0-9]{1}[0-3]{1}[0-9]{1}[HM]{1}[0-9]{3}',
    message='El INE no tiene un formato válido',
    code='ine_invalido'
)

curp_validador = RegexValidator(
    regex=r'^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$',
    message='El CURP no tiene un formato valido',
    code='curp_invalido'
)
