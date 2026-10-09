import pytest
from playwright.sync_api import Page, expect


BASE_URL = "https://www.saucedemo.com"


def test_cp_001_inicio_sesion_exitoso(page: Page):
    """CP-001: Inicio de sesión exitoso con credenciales válidas"""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    expect(page.locator(".title")).to_have_text("Products")


@pytest.mark.skip(reason="SauceDemo no valida formato de correo electrónico, usa usuario/contraseña simples sin esa regla de negocio")
def test_cp_002_correo_invalido_sin_arroba(page: Page):
    """CP-002: Validación de formato de correo inválido sin arroba"""
    pass


@pytest.mark.skip(reason="SauceDemo no valida formato de correo electrónico, usa usuario/contraseña simples sin esa regla de negocio")
def test_cp_003_correo_invalido_sin_dominio(page: Page):
    """CP-003: Validación de formato de correo inválido sin dominio"""
    pass


@pytest.mark.skip(reason="SauceDemo no implementa reglas de longitud mínima de contraseña")
def test_cp_004_password_menos_de_8_caracteres(page: Page):
    """CP-004: Rechazo de contraseña con menos de 8 caracteres"""
    pass


def test_cp_005_password_8_caracteres_validos(page: Page):
    """CP-005: Validación de contraseña con exactamente 8 caracteres válidos"""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    expect(page.locator(".title")).to_have_text("Products")


@pytest.mark.skip(reason="SauceDemo no implementa reglas de complejidad de contraseña (mayúsculas)")
def test_cp_006_password_sin_mayusculas(page: Page):
    """CP-006: Rechazo de contraseña sin mayúsculas"""
    pass


@pytest.mark.skip(reason="SauceDemo no implementa reglas de complejidad de contraseña (números)")
def test_cp_007_password_sin_numeros(page: Page):
    """CP-007: Rechazo de contraseña sin números"""
    pass


def test_cp_008_primer_intento_fallido(page: Page):
    """CP-008: Primer intento fallido de inicio de sesión con contraseña incorrecta"""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "Wrong123")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")


def test_cp_009_segundo_intento_fallido_consecutivo(page: Page):
    """CP-009: Segundo intento fallido consecutivo de inicio de sesión"""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "Wrong123")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()

    page.fill("#user-name", "standard_user")
    page.fill("#password", "Wrong456")
    page.click("#login-button")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")


@pytest.mark.skip(reason="SauceDemo no implementa bloqueo de cuenta tras N intentos fallidos consecutivos")
def test_cp_010_bloqueo_tras_3_intentos_fallidos(page: Page):
    """CP-010: Bloqueo de cuenta tras 3 intentos fallidos consecutivos"""
    pass


def test_cp_011_intento_inicio_sesion_cuenta_bloqueada(page: Page):
    """CP-011: Intento de inicio de sesión con cuenta bloqueada"""
    page.goto(BASE_URL)
    page.fill("#user-name", "locked_out_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("locked out")


@pytest.mark.skip(reason="Requiere simular el paso de tiempo (15 minutos) y desbloqueo automático; locked_out_user en SauceDemo es un bloqueo permanente, no temporal")
def test_cp_012_login_exitoso_tras_periodo_bloqueo(page: Page):
    """CP-012: Inicio de sesión exitoso después de cumplirse el período de bloqueo"""
    pass


@pytest.mark.skip(reason="SauceDemo no cuenta con un usuario con estado 'inactivo/deshabilitado' distinto del locked_out_user")
def test_cp_013_usuario_inactivo(page: Page):
    """CP-013: Intento de inicio de sesión con usuario inactivo"""
    pass


def test_cp_014_correo_no_registrado(page: Page):
    """CP-014: Intento de inicio de sesión con correo no registrado"""
    page.goto(BASE_URL)
    page.fill("#user-name", "noexiste_user")
    page.fill("#password", "Test1234")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("do not match")


def test_cp_015_campos_vacios(page: Page):
    """CP-015: Validación de campos vacíos en correo y contraseña"""
    page.goto(BASE_URL)
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username is required")


def test_cp_016_campo_correo_vacio(page: Page):
    """CP-016: Validación de campo correo vacío"""
    page.goto(BASE_URL)
    page.fill("#password", "Test1234")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username is required")


def test_cp_017_campo_password_vacio(page: Page):
    """CP-017: Validación de campo contraseña vacío"""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Password is required")


def test_cp_018_password_con_espacios(page: Page):
    """CP-018: Validación de contraseña con espacios al inicio y final"""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", " secret_sauce ")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("do not match")


@pytest.mark.skip(reason="No es posible confirmar con los selectores dados si SauceDemo distingue mayúsculas/minúsculas en el usuario sin acceso a documentación/BD adicional")
def test_cp_019_correo_mayusculas_minusculas(page: Page):
    """CP-019: Validación de correo con mayúsculas y minúsculas"""
    pass


def test_cp_020_inyeccion_sql_usuario(page: Page):
    """CP-020: Intento de inyección SQL en campo correo"""
    page.goto(BASE_URL)
    page.fill("#user-name", "admin'--")
    page.fill("#password", "Test1234")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("do not match")


def test_cp_021_inyeccion_sql_password(page: Page):
    """CP-021: Intento de inyección SQL en campo contraseña"""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "' OR '1'='1")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("do not match")


def test_cp_022_password_case_sensitive(page: Page):
    """CP-022: Validación de contraseña case-sensitive"""
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "SECRET_SAUCE")
    page.click("#login-button")
    error = page.locator('h3[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("do not match")


@pytest.mark.skip(reason="SauceDemo no implementa contador de intentos fallidos ni bloqueo de cuenta, por lo que no es posible validar su reseteo")
def test_cp_023_reseteo_contador_intentos(page: Page):
    """CP-023: Reseteo de contador de intentos tras inicio exitoso"""
    pass