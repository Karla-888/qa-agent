import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://the-internet.herokuapp.com/login"


def test_bas_01_login_exitoso_area_segura(page: Page):
    """
    BAS-01: Autenticacion exitosa con usuario y contrasena validos, redireccion al area segura y mensaje de bienvenida
    """
    page.goto(BASE_URL)
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button[type='submit']")

    expect(page.locator("h2")).to_have_text("Secure Area")
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")


@pytest.mark.skip(
    reason="No se proporciono el selector del boton/enlace de cerrar sesion, "
    "por lo que no es posible automatizar el paso de logout con los selectores dados."
)
def test_bas_02_cierre_sesion_exitoso(page: Page):
    """
    BAS-02: Cierre de sesion exitoso desde el area segura
    """
    page.goto(BASE_URL)
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button[type='submit']")

    # No existe selector definido para el enlace/boton de cerrar sesion.
    pass


def test_alt_01_login_usuario_inexistente(page: Page):
    """
    ALT-01: Intento de login con nombre de usuario inexistente
    """
    page.goto(BASE_URL)
    page.fill("#username", "usuario_inexistente")
    page.fill("#password", "ClaveCualquiera1!")
    page.click("button[type='submit']")

    expect(page.locator("#flash")).to_contain_text("invalid")
    expect(page).to_have_url(BASE_URL)


def test_alt_02_login_contrasena_incorrecta(page: Page):
    """
    ALT-02: Intento de login con usuario existente y contrasena incorrecta
    """
    page.goto(BASE_URL)
    page.fill("#username", "juan.perez")
    page.fill("#password", "ClaveIncorrecta9!")
    page.click("button[type='submit']")

    expect(page.locator("#flash")).to_contain_text("invalid")
    expect(page).to_have_url(BASE_URL)


def test_alt_03_login_campos_vacios(page: Page):
    """
    ALT-03: Intento de login con campos Usuario y Contrasena vacios
    """
    page.goto(BASE_URL)
    page.fill("#username", "")
    page.fill("#password", "")
    page.click("button[type='submit']")

    expect(page.locator("#flash")).to_be_visible()
    expect(page).to_have_url(BASE_URL)


@pytest.mark.skip(
    reason="Automatizable: No. Requiere acceso directo a la base de datos para "
    "verificar el hash de la contrasena almacenado, lo cual no es posible mediante "
    "pruebas de interfaz con Playwright."
)
def test_int_01_integridad_contrasena_no_se_altera(page: Page):
    """
    INT-01: Verificar que la contrasena almacenada en base de datos no se altera tras multiples intentos fallidos de autenticacion
    """
    pass


@pytest.mark.skip(
    reason="Automatizable: No. Requiere acceso directo al almacenamiento de sesiones "
    "del backend para verificar la eliminacion del registro de sesion, lo cual no es "
    "posible mediante pruebas de interfaz con Playwright."
)
def test_int_02_integridad_sesion_eliminada_al_logout(page: Page):
    """
    INT-02: Verificar que la sesion del usuario se elimina correctamente del backend al cerrar sesion
    """
    pass