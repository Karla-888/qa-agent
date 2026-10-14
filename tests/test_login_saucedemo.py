import pytest
from playwright.sync_api import Page, expect

LOGIN_URL = "https://www.saucedemo.com"


def test_bas_01_inicio_sesion_exitoso_credenciales_validas(page: Page):
    """
    BAS-01: Inicio de sesión exitoso con correo y contraseña válidos
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page.locator(".title")).to_have_text("Products")


@pytest.mark.skip(
    reason="SauceDemo no valida formato de correo, solo compara usuario y contraseña "
    "contra una lista fija. No existe mensaje 'Formato de correo inválido' ni "
    "resaltado de campo erróneo, por lo que el resultado esperado no puede verificarse."
)
def test_alt_01_formato_correo_invalido(page: Page):
    """
    ALT-01: Intento de inicio de sesión con formato de correo inválido
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "usuarioarroba.dominio.com")
    page.fill("#password", "Clave123")
    page.click("#login-button")

    expect(page.locator('h3[data-test="error"]')).to_contain_text("Formato de correo inválido")


@pytest.mark.skip(
    reason="SauceDemo no implementa reglas de complejidad de contraseña (mínimo 8 "
    "caracteres, mayúscula, número). No existe el mensaje esperado en el sitio, "
    "por lo que el resultado esperado no puede verificarse."
)
def test_alt_02_contrasena_menos_8_caracteres(page: Page):
    """
    ALT-02: Intento de inicio de sesión con contraseña de menos de 8 caracteres
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "usuario@dominio.com")
    page.fill("#password", "Cla12")
    page.click("#login-button")

    expect(page.locator('h3[data-test="error"]')).to_contain_text(
        "La contraseña debe tener mínimo 8 caracteres, una mayúscula y un número"
    )


@pytest.mark.skip(
    reason="SauceDemo no implementa reglas de complejidad de contraseña (mayúscula "
    "obligatoria). No existe el mensaje esperado en el sitio, por lo que el "
    "resultado esperado no puede verificarse."
)
def test_alt_03_contrasena_sin_mayuscula(page: Page):
    """
    ALT-03: Intento de inicio de sesión con contraseña sin mayúscula
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "usuario@dominio.com")
    page.fill("#password", "clave123")
    page.click("#login-button")

    expect(page.locator('h3[data-test="error"]')).to_contain_text(
        "La contraseña debe tener mínimo 8 caracteres, una mayúscula y un número"
    )


@pytest.mark.skip(
    reason="SauceDemo no implementa reglas de complejidad de contraseña (número "
    "obligatorio). No existe el mensaje esperado en el sitio, por lo que el "
    "resultado esperado no puede verificarse."
)
def test_alt_04_contrasena_sin_numero(page: Page):
    """
    ALT-04: Intento de inicio de sesión con contraseña sin número
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "usuario@dominio.com")
    page.fill("#password", "Claveabc")
    page.click("#login-button")

    expect(page.locator('h3[data-test="error"]')).to_contain_text(
        "La contraseña debe tener mínimo 8 caracteres, una mayúscula y un número"
    )


@pytest.mark.skip(
    reason="Caso marcado como no automatizable: requiere control de tiempo real de "
    "bloqueo, validar manualmente o con mock de reloj."
)
def test_alt_05_bloqueo_cuenta_tres_intentos_fallidos(page: Page):
    """
    ALT-05: Bloqueo de cuenta tras 3 intentos fallidos consecutivos
    """
    page.goto(LOGIN_URL)
    for clave in ["ClaveMala1", "ClaveMala2", "ClaveMala3"]:
        page.fill("#user-name", "usuario@dominio.com")
        page.fill("#password", clave)
        page.click("#login-button")
        expect(page.locator('h3[data-test="error"]')).to_contain_text("Credenciales incorrectas")

    page.fill("#user-name", "usuario@dominio.com")
    page.fill("#password", "Clave123")
    page.click("#login-button")
    expect(page.locator('h3[data-test="error"]')).to_contain_text(
        "Cuenta bloqueada, intente en 15 minutos"
    )


@pytest.mark.skip(
    reason="Caso marcado como no automatizable: requiere estado previo de usuario "
    "inactivo en base de datos."
)
def test_alt_06_usuario_inactivo_intenta_login(page: Page):
    """
    ALT-06: Usuario inactivo intenta iniciar sesión
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "inactivo@dominio.com")
    page.fill("#password", "Clave123")
    page.click("#login-button")

    expect(page.locator('h3[data-test="error"]')).to_contain_text("Usuario deshabilitado")


@pytest.mark.skip(
    reason="Caso marcado como no automatizable: requiere estado previo de bloqueo "
    "en base de datos."
)
def test_alt_07_intento_login_durante_bloqueo_activo(page: Page):
    """
    ALT-07: Intento de inicio de sesión durante periodo de bloqueo activo
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "usuario@dominio.com")
    page.fill("#password", "Clave123")
    page.click("#login-button")

    expect(page.locator('h3[data-test="error"]')).to_contain_text(
        "Cuenta bloqueada, intente en 15 minutos"
    )


def test_alt_08_contrasena_incorrecta_primer_intento(page: Page):
    """
    ALT-08: Intento de inicio de sesión con contraseña incorrecta en primer intento
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "ClaveMala1")
    page.click("#login-button")

    expect(page.locator('h3[data-test="error"]')).to_be_visible()
    expect(page.locator(".title")).not_to_be_visible()


@pytest.mark.skip(
    reason="Caso marcado como no automatizable: requiere estado previo de intentos "
    "fallidos en base de datos y consulta directa a BD."
)
def test_int_01_contador_intentos_fallidos_reinicio(page: Page):
    """
    INT-01: El contador de intentos fallidos se reinicia tras un inicio de sesión exitoso
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "usuario@dominio.com")
    page.fill("#password", "Clave123")
    page.click("#login-button")

    expect(page.locator(".title")).to_have_text("Products")


@pytest.mark.skip(
    reason="Caso marcado como no automatizable: requiere manipulación de tiempos de "
    "bloqueo en base de datos, no automatizable por tiempos de espera largos."
)
def test_int_02_reautenticacion_tras_expirar_bloqueo(page: Page):
    """
    INT-02: El usuario puede autenticarse nuevamente tras expirar el bloqueo de 15 minutos
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "usuario@dominio.com")
    page.fill("#password", "Clave123")
    page.click("#login-button")

    expect(page.locator(".title")).to_have_text("Products")


@pytest.mark.skip(
    reason="Caso marcado como no automatizable: requiere acceso al módulo de "
    "administración y estado previo en base de datos."
)
def test_int_03_consistencia_estado_inactivo_admin_login(page: Page):
    """
    INT-03: Consistencia del estado inactivo del usuario entre el módulo de administración y el módulo de login
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "usuario2@dominio.com")
    page.fill("#password", "Clave123")
    page.click("#login-button")

    expect(page.locator('h3[data-test="error"]')).to_contain_text("Usuario deshabilitado")


@pytest.mark.skip(
    reason="Caso marcado como no automatizable: prueba de desempeño, requiere "
    "herramienta de carga y ambiente dedicado."
)
def test_otr_01_tiempo_respuesta_login_carga_normal(page: Page):
    """
    OTR-01: Tiempo de respuesta del proceso de inicio de sesión bajo carga normal
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page.locator(".title")).to_have_text("Products")


@pytest.mark.skip(
    reason="Caso marcado como no automatizable: requiere validación manual en "
    "múltiples navegadores o suite de pruebas cross-browser."
)
def test_otr_02_compatibilidad_formulario_login_navegadores(page: Page):
    """
    OTR-02: Compatibilidad del formulario de inicio de sesión en distintos navegadores
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page.locator(".title")).to_have_text("Products")


@pytest.mark.skip(
    reason="Caso marcado como no automatizable: el requerimiento no especifica "
    "soporte móvil explícitamente, se marca como supuesto."
)
def test_otr_03_responsividad_formulario_login_movil(page: Page):
    """
    OTR-03: Responsividad del formulario de inicio de sesión en dispositivo móvil
    """
    page.goto(LOGIN_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page.locator(".title")).to_have_text("Products")