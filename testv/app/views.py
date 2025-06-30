from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse

# Create your views here.
def login(request):
    return render(request, 'app/login.html')

def proveedor(request):
    url = 'http://13.218.8.124/ordenes/obtener/'
    payload = {"id_proveedor": "1"}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        datos = response.json()
    except Exception as e:
        datos = []
        print("Error al consultar la API:", e)

    return render(request, 'app/proveedor/proveedor.html', {'ordenes': datos, 'id_proveedor': 1})


def detalleorden(request, codigo):
    url = 'http://13.218.8.124/orden/obtener/'  # Usa el endpoint correcto de tu API
    payload = {"codigo": codigo}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        datos = response.json()
    except Exception as e:
        datos = None
        print("Error al consultar la API:", e)

    return render(request, 'app/proveedor/detalleorden.html', {'orden': datos, 'codigo': codigo})

def admin2(request):
    url = 'http://34.194.212.252/api/prov/'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        proveedores = response.json()
    except Exception as e:
        proveedores = []
        print("Error al consultar la API de proveedores:", e)

    return render(request, 'app/admin/admin.html', {'proveedores': proveedores})

def detalleproveedor(request, id_proveedor):
    # Obtén los datos del proveedor
    url_proveedor = f'http://34.194.212.252/api/prov/{id_proveedor}/'
    # Obtén todos los productos
    url_productos = 'http://34.194.212.252/api/prod_proveedor/'
    try:
        resp_prov = requests.get(url_proveedor, timeout=5)
        resp_prov.raise_for_status()
        proveedor = resp_prov.json()
    except Exception as e:
        proveedor = None
        print("Error proveedor:", e)

    try:
        resp_prods = requests.get(url_productos, timeout=5)
        resp_prods.raise_for_status()
        todos_productos = resp_prods.json()
    except Exception as e:
        todos_productos = []
        print("Error productos:", e)

    # Filtra los productos por el id_proveedor
    productos = [prod for prod in todos_productos if prod.get("id_proveedor") == id_proveedor]

    return render(request, 'app/admin/detalleprov.html', {
        'proveedor': proveedor,
        'productos': productos,
    })

def detalleproducto(request, id_producto):
    url_prod = 'http://34.194.212.252/api/prod_proveedor/'
    url_tipo = 'http://34.194.212.252/api/tipo/'
    url_marca = 'http://34.194.212.252/api/marca/'

    producto = None
    tipo_nombre = ''
    marca_nombre = ''
    id_proveedor = ''

    try:
        # Obtener todos los productos
        response = requests.get(url_prod, timeout=5)
        response.raise_for_status()
        productos = response.json()
        producto = next((p for p in productos if p["id_producto"] == id_producto), None)
        if producto:
            id_proveedor = producto["id_proveedor"]

            # Obtener tipos
            response_tipo = requests.get(url_tipo, timeout=5)
            response_tipo.raise_for_status()
            tipos = response_tipo.json()
            tipo = next((t for t in tipos if t["id_tipo"] == producto["id_tipo"]), None)
            tipo_nombre = tipo["nombre_tipo"] if tipo else ''

            # Obtener marcas
            response_marca = requests.get(url_marca, timeout=5)
            response_marca.raise_for_status()
            marcas = response_marca.json()
            marca = next((m for m in marcas if m["id_marca"] == producto["id_marca"]), None)
            marca_nombre = marca["nombre_marca"] if marca else ''
    except Exception as e:
        print("Error al consultar la API de productos, tipos o marcas:", e)

    return render(request, 'app/admin/detalleproducto.html', {
        'producto': producto,
        'id_proveedor': id_proveedor,
        'tipo_nombre': tipo_nombre,
        'marca_nombre': marca_nombre
    })

def prod_crear(request, id_proveedor):
    url_tipo = "http://34.194.212.252/api/tipo/"
    url_marca = "http://34.194.212.252/api/marca/"
    tipos, marcas = [], []

    # Cargar tipos y marcas para el formulario
    try:
        resp_tipo = requests.get(url_tipo, timeout=5)
        resp_tipo.raise_for_status()
        tipos = resp_tipo.json()
    except Exception as e:
        print("Error cargando tipos:", e)

    try:
        resp_marca = requests.get(url_marca, timeout=5)
        resp_marca.raise_for_status()
        marcas = resp_marca.json()
    except Exception as e:
        print("Error cargando marcas:", e)

    # Si se envía el formulario (POST)
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        id_marca = request.POST.get("marca")
        id_tipo = request.POST.get("tipo")

        data = {
            "nombre_producto": nombre,
            "descripcion": descripcion,
            "precio": int(precio),
            "id_proveedor": id_proveedor,
            "id_marca": int(id_marca),
            "id_tipo": int(id_tipo)
        }
        # Hacer POST a la API
        url_post = "http://34.194.212.252/api/prod_proveedor/"
        try:
            resp = requests.post(url_post, json=data, timeout=5)
            resp.raise_for_status()
            # Redirigir al detalle del proveedor tras crear
            return redirect('detalleproveedor', id_proveedor=id_proveedor)
        except Exception as e:
            print("Error creando producto:", e)
            error = "No se pudo crear el producto."
            return render(request, "app/admin/prod_crear.html", {
                "tipos": tipos,
                "marcas": marcas,
                "id_proveedor": id_proveedor,
                "error": error
            })

    # GET normal
    return render(request, "app/admin/prod_crear.html", {
        "tipos": tipos,
        "marcas": marcas,
        "id_proveedor": id_proveedor
    })

def prod_editar(request, id_producto):
    url_productos = "http://34.194.212.252/api/prod_proveedor/"
    url_tipo = "http://34.194.212.252/api/tipo/"
    url_marca = "http://34.194.212.252/api/marca/"

    producto = None
    tipos = []
    marcas = []
    id_proveedor = ""

    # Cargar datos del producto
    try:
        resp_prod = requests.get(url_productos, timeout=5)
        resp_prod.raise_for_status()
        productos = resp_prod.json()
        producto = next((p for p in productos if p["id_producto"] == id_producto), None)
        if producto:
            id_proveedor = producto["id_proveedor"]
    except Exception as e:
        print("Error cargando producto:", e)

    # Cargar tipos y marcas
    try:
        resp_tipo = requests.get(url_tipo, timeout=5)
        resp_tipo.raise_for_status()
        tipos = resp_tipo.json()
    except Exception as e:
        print("Error cargando tipos:", e)

    try:
        resp_marca = requests.get(url_marca, timeout=5)
        resp_marca.raise_for_status()
        marcas = resp_marca.json()
    except Exception as e:
        print("Error cargando marcas:", e)

    # Si envia el formulario (POST)
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        id_marca = request.POST.get("marca")
        id_tipo = request.POST.get("tipo")

        data = {
            "nombre_producto": nombre,
            "descripcion": descripcion,
            "precio": int(precio),
            "id_proveedor": id_proveedor,
            "id_marca": int(id_marca),
            "id_tipo": int(id_tipo)
        }
        url_put = f"http://34.194.212.252/api/prod_proveedor/{id_producto}/"
        try:
            resp = requests.put(url_put, json=data, timeout=5)
            resp.raise_for_status()
            # Redirigir al detalle del proveedor tras editar
            return redirect('detalleproveedor', id_proveedor=id_proveedor)
        except Exception as e:
            print("Error editando producto:", e)
            error = "No se pudo editar el producto."
            return render(request, "app/admin/prod_editar.html", {
                "tipos": tipos,
                "marcas": marcas,
                "producto": producto,
                "id_proveedor": id_proveedor,
                "id_producto": id_producto,
                "error": error
            })

    # GET normal
    return render(request, "app/admin/prod_editar.html", {
        "tipos": tipos,
        "marcas": marcas,
        "producto": producto,
        "id_proveedor": id_proveedor,
        "id_producto": id_producto
    })

def prod_eliminar(request, id_producto):
    if request.method == "POST":
        # Opcional: primero busca el producto para obtener el id_proveedor
        url_get = "http://34.194.212.252/api/prod_proveedor/"
        try:
            resp = requests.get(url_get, timeout=5)
            resp.raise_for_status()
            productos = resp.json()
            producto = next((p for p in productos if p["id_producto"] == id_producto), None)
            id_proveedor = producto["id_proveedor"] if producto else ""
        except Exception as e:
            print("Error buscando producto para eliminar:", e)
            id_proveedor = ""

        # Ahora elimina
        url_delete = f"http://34.194.212.252/api/prod_proveedor/{id_producto}/"
        try:
            resp = requests.delete(url_delete, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            print("Error eliminando producto:", e)
        # Redirige al detalle del proveedor
        return redirect('detalleproveedor', id_proveedor=id_proveedor)

def proveedor_crear(request):
    error = None
    data = None
    if request.method == "POST":
        correo = request.POST.get("correo")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        telefono = request.POST.get("telefono")
        rut = request.POST.get("rut")
        dv = request.POST.get("dv")
        nombre_empresa = request.POST.get("nombre_empresa")
        pais_empresa = request.POST.get("pais_empresa")
        rut_empresa = request.POST.get("rut_empresa")
        puntuacion = request.POST.get("puntuacion", 0)

        try:
            data = {
                "correo": correo,
                "nombre": nombre,
                "apellido": apellido,
                "telefono": telefono,
                "rut": int(rut),
                "dv": dv,
                "nombre_empresa": nombre_empresa,
                "pais_empresa": pais_empresa,
                "rut_empresa": int(rut_empresa),
                "puntuacion": int(puntuacion)
            }
        except Exception as e:
            print("Error armando el diccionario data:", e)
            error = f"Error en los datos ingresados: {e}"
            return render(request, "app/admin/prov_crear.html", {"error": error})

        url_post = "http://34.194.212.252/api/prov/"
        print("Intentando crear proveedor en:", url_post)
        print("Datos a enviar:", data)
        try:
            resp = requests.post(url_post, json=data, timeout=5)
            print("Status code:", resp.status_code)
            print("Respuesta del servidor:", resp.text)
            resp.raise_for_status()
            return redirect('admin2')
        except requests.exceptions.RequestException as e:
            print("Error creando proveedor:", e)
            if hasattr(e, 'response') and e.response is not None:
                print("Mensaje de error del backend:", e.response.text)
            error = f"No se pudo crear el proveedor. {e}"
    return render(request, "app/admin/prov_crear.html", {
        "error": error
    })
