from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn

app = FastAPI(title="Sistema de Inventario API", version="1.0.0")

# CRUD generico server-side (persistencia multi-dispositivo)
try:
    from app.routers import data as _data_router
    app.include_router(_data_router.router)
except Exception as _e:
    import logging; logging.getLogger('uvicorn').warning('data router: %s', _e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Pydantic Models ──────────────────────────────────────────────────────────

class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: str
    activa: bool = True

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activa: Optional[bool] = None

class ProveedorCreate(BaseModel):
    nombre: str
    contacto: str
    email: str
    telefono: str
    direccion: str
    activo: bool = True

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = None
    contacto: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = None

class ProductoCreate(BaseModel):
    nombre: str
    sku: str
    descripcion: str
    precio: float
    costo: float
    stock: int
    stock_minimo: int
    categoria_id: int
    proveedor_id: int
    activo: bool = True

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    sku: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    costo: Optional[float] = None
    stock: Optional[int] = None
    stock_minimo: Optional[int] = None
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    activo: Optional[bool] = None

class MovimientoCreate(BaseModel):
    producto_id: int
    tipo: str
    cantidad: int
    motivo: str
    usuario: str

class MovimientoUpdate(BaseModel):
    motivo: Optional[str] = None
    usuario: Optional[str] = None


# ─── Seed Data ────────────────────────────────────────────────────────────────

categorias_db: List[dict] = [
    {"id": 1, "nombre": "Electrónica", "descripcion": "Dispositivos electrónicos y accesorios tecnológicos", "activa": True},
    {"id": 2, "nombre": "Herramientas", "descripcion": "Herramientas manuales y eléctricas para obra", "activa": True},
    {"id": 3, "nombre": "Papelería", "descripcion": "Material de oficina, papelería y útiles escolares", "activa": True},
    {"id": 4, "nombre": "Limpieza", "descripcion": "Productos de limpieza, higiene e insumos sanitarios", "activa": True},
    {"id": 5, "nombre": "Mobiliario", "descripcion": "Muebles, sillas y elementos de ambientación", "activa": False},
    {"id": 6, "nombre": "Seguridad", "descripcion": "Equipos de protección personal y seguridad industrial", "activa": True},
]

proveedores_db: List[dict] = [
    {"id": 1, "nombre": "TechDistrib S.A.", "contacto": "Carlos Mendoza", "email": "carlos@techdistrib.com", "telefono": "+54 11 4567-8901", "direccion": "Av. Corrientes 1234, CABA", "activo": True},
    {"id": 2, "nombre": "Herramientas del Sur", "contacto": "Laura Gómez", "email": "lgomez@herramisur.com", "telefono": "+54 11 3456-7890", "direccion": "Av. Rivadavia 5678, CABA", "activo": True},
    {"id": 3, "nombre": "Papelera Central", "contacto": "Martín Ruiz", "email": "mruiz@papcentral.com", "telefono": "+54 11 2345-6789", "direccion": "Calle Florida 890, CABA", "activo": True},
    {"id": 4, "nombre": "CleanPro Argentina", "contacto": "Ana Torres", "email": "atorres@cleanpro.com.ar", "telefono": "+54 11 1234-5678", "direccion": "Av. Santa Fe 321, CABA", "activo": True},
    {"id": 5, "nombre": "MegaSupplies SRL", "contacto": "Roberto Díaz", "email": "rdiaz@megasupplies.com", "telefono": "+54 11 9876-5432", "direccion": "Av. Belgrano 4567, CABA", "activo": False},
    {"id": 6, "nombre": "SafeGuard Industrial", "contacto": "Verónica Paredes", "email": "vparedes@safeguard.com.ar", "telefono": "+54 11 8765-4321", "direccion": "Av. Entre Ríos 789, CABA", "activo": True},
]

productos_db: List[dict] = [
    {"id": 1, "nombre": "Laptop HP 15\"", "sku": "LAP-HP-001", "descripcion": "Laptop HP 15 pulgadas, Intel Core i5, 8GB RAM, 256GB SSD", "precio": 850000.00, "costo": 650000.00, "stock": 12, "stock_minimo": 3, "categoria_id": 1, "proveedor_id": 1, "activo": True},
    {"id": 2, "nombre": "Mouse Inalámbrico Logitech M185", "sku": "MOU-LOG-001", "descripcion": "Mouse inalámbrico Logitech M185, receptor nano USB 2.4GHz", "precio": 8500.00, "costo": 5200.00, "stock": 45, "stock_minimo": 10, "categoria_id": 1, "proveedor_id": 1, "activo": True},
    {"id": 3, "nombre": "Teclado Mecánico RGB TKL", "sku": "TEC-RGB-001", "descripcion": "Teclado mecánico tenkeyless, retroiluminación RGB, switches blue", "precio": 25000.00, "costo": 16000.00, "stock": 8, "stock_minimo": 5, "categoria_id": 1, "proveedor_id": 1, "activo": True},
    {"id": 4, "nombre": "Taladro Inalámbrico Bosch 18V", "sku": "TAL-BOS-001", "descripcion": "Taladro percutor inalámbrico Bosch 18V, incluye 2 baterías y cargador", "precio": 95000.00, "costo": 68000.00, "stock": 6, "stock_minimo": 2, "categoria_id": 2, "proveedor_id": 2, "activo": True},
    {"id": 5, "nombre": "Set Destornilladores Stanley 12 pzas", "sku": "DES-STA-001", "descripcion": "Juego 12 piezas destornilladores Stanley, mango ergonómico bimateria", "precio": 18000.00, "costo": 11000.00, "stock": 20, "stock_minimo": 5, "categoria_id": 2, "proveedor_id": 2, "activo": True},
    {"id": 6, "nombre": "Resma Papel A4 x500", "sku": "PAP-A4-001", "descripcion": "Resma papel A4 75g/m², 500 hojas blancas, apto impresión láser e inkjet", "precio": 3200.00, "costo": 2100.00, "stock": 150, "stock_minimo": 30, "categoria_id": 3, "proveedor_id": 3, "activo": True},
    {"id": 7, "nombre": "Bolígrafos BIC Cristal x12", "sku": "BOL-BIC-001", "descripcion": "Pack 12 bolígrafos BIC cristal punta media 1.0mm, color azul", "precio": 1800.00, "costo": 950.00, "stock": 2, "stock_minimo": 20, "categoria_id": 3, "proveedor_id": 3, "activo": True},
    {"id": 8, "nombre": "Detergente Industrial 5L", "sku": "DET-IND-001", "descripcion": "Detergente industrial concentrado 5 litros, aroma limón, biodegradable", "precio": 4500.00, "costo": 2800.00, "stock": 35, "stock_minimo": 10, "categoria_id": 4, "proveedor_id": 4, "activo": True},
    {"id": 9, "nombre": "Casco de Seguridad MSA", "sku": "CAS-MSA-001", "descripcion": "Casco de seguridad industrial MSA V-Gard, clase E, color blanco", "precio": 12000.00, "costo": 7500.00, "stock": 18, "stock_minimo": 5, "categoria_id": 6, "proveedor_id": 6, "activo": True},
    {"id": 10, "nombre": "Monitor LG 24\" Full HD", "sku": "MON-LG-001", "descripcion": "Monitor LG 24 pulgadas IPS Full HD 1920x1080, 75Hz, HDMI+VGA", "precio": 120000.00, "costo": 88000.00, "stock": 4, "stock_minimo": 2, "categoria_id": 1, "proveedor_id": 1, "activo": True},
]

movimientos_db: List[dict] = [
    {"id": 1, "producto_id": 1, "tipo": "entrada", "cantidad": 10, "motivo": "Compra a proveedor - Orden de compra #OC-2024-001", "fecha": "2024-01-15T09:30:00", "usuario": "admin", "stock_anterior": 2, "stock_nuevo": 12},
    {"id": 2, "producto_id": 7, "tipo": "salida", "cantidad": 18, "motivo": "Venta a cliente - Factura #F001-00234", "fecha": "2024-01-16T14:20:00", "usuario": "almacen", "stock_anterior": 20, "stock_nuevo": 2},
    {"id": 3, "producto_id": 6, "tipo": "entrada", "cantidad": 100, "motivo": "Reposición de stock - Orden de compra #OC-2024-002", "fecha": "2024-01-17T10:00:00", "usuario": "admin", "stock_anterior": 50, "stock_nuevo": 150},
    {"id": 4, "producto_id": 4, "tipo": "salida", "cantidad": 2, "motivo": "Préstamo interno a obra - Remito #R-00567", "fecha": "2024-01-18T16:45:00", "usuario": "almacen", "stock_anterior": 8, "stock_nuevo": 6},
    {"id": 5, "producto_id": 2, "tipo": "ajuste", "cantidad": 5, "motivo": "Ajuste por inventario físico periódico - diferencia de conteo", "fecha": "2024-01-19T08:15:00", "usuario": "admin", "stock_anterior": 40, "stock_nuevo": 45},
    {"id": 6, "producto_id": 8, "tipo": "entrada", "cantidad": 20, "motivo": "Compra a proveedor - Orden de compra #OC-2024-003", "fecha": "2024-01-20T11:30:00", "usuario": "admin", "stock_anterior": 15, "stock_nuevo": 35},
    {"id": 7, "producto_id": 3, "tipo": "salida", "cantidad": 2, "motivo": "Venta a cliente - Factura #F001-00289", "fecha": "2024-01-21T15:00:00", "usuario": "almacen", "stock_anterior": 10, "stock_nuevo": 8},
    {"id": 8, "producto_id": 10, "tipo": "entrada", "cantidad": 4, "motivo": "Compra a proveedor - Orden de compra #OC-2024-004", "fecha": "2024-01-22T09:00:00", "usuario": "admin", "stock_anterior": 0, "stock_nuevo": 4},
]

_cat_counter = 7
_prov_counter = 7
_prod_counter = 11
_mov_counter = 9


# ─── CRUD Categorías ──────────────────────────────────────────────────────────

@app.get("/categorias", response_model=List[dict], tags=["Categorías"])
def get_categorias():
    return categorias_db

@app.get("/categorias/{categoria_id}", response_model=dict, tags=["Categorías"])
def get_categoria(categoria_id: int):
    item = next((c for c in categorias_db if c["id"] == categoria_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return item

@app.post("/categorias", response_model=dict, status_code=201, tags=["Categorías"])
def create_categoria(data: CategoriaCreate):
    global _cat_counter
    nuevo = {"id": _cat_counter, **data.dict()}
    _cat_counter += 1
    categorias_db.append(nuevo)
    return nuevo

@app.put("/categorias/{categoria_id}", response_model=dict, tags=["Categorías"])
def update_categoria(categoria_id: int, data: CategoriaUpdate):
    idx = next((i for i, c in enumerate(categorias_db) if c["id"] == categoria_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    patch = {k: v for k, v in data.dict().items() if v is not None}
    categorias_db[idx].update(patch)
    return categorias_db[idx]

@app.delete("/categorias/{categoria_id}", response_model=dict, tags=["Categorías"])
def delete_categoria(categoria_id: int):
    idx = next((i for i, c in enumerate(categorias_db) if c["id"] == categoria_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    deleted = categorias_db.pop(idx)
    return {"mensaje": "Categoría eliminada", "id": deleted["id"]}


# ─── CRUD Proveedores ─────────────────────────────────────────────────────────

@app.get("/proveedores", response_model=List[dict], tags=["Proveedores"])
def get_proveedores():
    return proveedores_db

@app.get("/proveedores/{proveedor_id}", response_model=dict, tags=["Proveedores"])
def get_proveedor(proveedor_id: int):
    item = next((p for p in proveedores_db if p["id"] == proveedor_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return item

@app.post("/proveedores", response_model=dict, status_code=201, tags=["Proveedores"])
def create_proveedor(data: ProveedorCreate):
    global _prov_counter
    nuevo = {"id": _prov_counter, **data.dict()}
    _prov_counter += 1
    proveedores_db.append(nuevo)
    return nuevo

@app.put("/proveedores/{proveedor_id}", response_model=dict, tags=["Proveedores"])
def update_proveedor(proveedor_id: int, data: ProveedorUpdate):
    idx = next((i for i, p in enumerate(proveedores_db) if p["id"] == proveedor_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    patch = {k: v for k, v in data.dict().items() if v is not None}
    proveedores_db[idx].update(patch)
    return proveedores_db[idx]

@app.delete("/proveedores/{proveedor_id}", response_model=dict, tags=["Proveedores"])
def delete_proveedor(proveedor_id: int):
    idx = next((i for i, p in enumerate(proveedores_db) if p["id"] == proveedor_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    deleted = proveedores_db.pop(idx)
    return {"mensaje": "Proveedor eliminado", "id": deleted["id"]}


# ─── CRUD Productos ───────────────────────────────────────────────────────────

@app.get("/productos", response_model=List[dict], tags=["Productos"])
def get_productos():
    return productos_db

@app.get("/productos/{producto_id}", response_model=dict, tags=["Productos"])
def get_producto(producto_id: int):
    item = next((p for p in productos_db if p["id"] == producto_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@app.post("/productos", response_model=dict, status_code=201, tags=["Productos"])
def create_producto(data: ProductoCreate):
    global _prod_counter
    cat = next((c for c in categorias_db if c["id"] == data.categoria_id), None)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    prov = next((p for p in proveedores_db if p["id"] == data.proveedor_id), None)
    if not prov:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    sku_existe = next((p for p in productos_db if p["sku"] == data.sku), None)
    if sku_existe:
        raise HTTPException(status_code=400, detail=f"Ya existe un producto con el SKU '{data.sku}'")
    nuevo = {"id": _prod_counter, **data.dict()}
    _prod_counter += 1
    productos_db.append(nuevo)
    return nuevo

@app.put("/productos/{producto_id}", response_model=dict, tags=["Productos"])
def update_producto(producto_id: int, data: ProductoUpdate):
    idx = next((i for i, p in enumerate(productos_db) if p["id"] == producto_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    patch = {k: v for k, v in data.dict().items() if v is not None}
    if "sku" in patch:
        sku_existe = next((p for p in productos_db if p["sku"] == patch["sku"] and p["id"] != producto_id), None)
        if sku_existe:
            raise HTTPException(status_code=400, detail=f"Ya existe un producto con el SKU '{patch['sku']}'")
    productos_db[idx].update(patch)
    return productos_db[idx]

@app.delete("/productos/{producto_id}", response_model=dict, tags=["Productos"])
def delete_producto(producto_id: int):
    idx = next((i for i, p in enumerate(productos_db) if p["id"] == producto_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    deleted = productos_db.pop(idx)
    return {"mensaje": "Producto eliminado", "id": deleted["id"]}


# ─── CRUD MovimientosStock ────────────────────────────────────────────────────

@app.get("/movimientos", response_model=List[dict], tags=["Movimientos"])
def get_movimientos():
    return sorted(movimientos_db, key=lambda m: m["fecha"], reverse=True)

@app.get("/movimientos/producto/{producto_id}", response_model=List[dict], tags=["Movimientos"])
def get_movimientos_by_producto(producto_id: int):
    resultado = [m for m in movimientos_db if m["producto_id"] == producto_id]
    return sorted(resultado, key=lambda m: m["fecha"], reverse=True)

@app.get("/movimientos/{movimiento_id}", response_model=dict, tags=["Movimientos"])
def get_movimiento(movimiento_id: int):
    item = next((m for m in movimientos_db if m["id"] == movimiento_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return item

@app.post("/movimientos", response_model=dict, status_code=201, tags=["Movimientos"])
def create_movimiento(data: MovimientoCreate):
    global _mov_counter
    tipos_validos = ["entrada", "salida", "ajuste"]
    if data.tipo not in tipos_validos:
        raise HTTPException(status_code=400, detail=f"Tipo inválido. Use: {', '.join(tipos_validos)}")
    if data.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

    prod_idx = next((i for i, p in enumerate(productos_db) if p["id"] == data.producto_id), None)
    if prod_idx is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto = productos_db[prod_idx]
    stock_anterior = producto["stock"]

    if data.tipo == "entrada":
        stock_nuevo = stock_anterior + data.cantidad
    elif data.tipo == "salida":
        if stock_anterior < data.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente. Stock actual: {stock_anterior}, solicitado: {data.cantidad}"
            )
        stock_nuevo = stock_anterior - data.cantidad
    else:
        stock_nuevo = data.cantidad

    productos_db[prod_idx]["stock"] = stock_nuevo

    nuevo = {
        "id": _mov_counter,
        "producto_id": data.producto_id,
        "tipo": data.tipo,
        "cantidad": data.cantidad,
        "motivo": data.motivo,
        "fecha": datetime.now().isoformat(),
        "usuario": data.usuario,
        "stock_anterior": stock_anterior,
        "stock_nuevo": stock_nuevo,
    }
    _mov_counter += 1
    movimientos_db.append(nuevo)
    return nuevo

@app.put("/movimientos/{movimiento_id}", response_model=dict, tags=["Movimientos"])
def update_movimiento(movimiento_id: int, data: MovimientoUpdate):
    idx = next((i for i, m in enumerate(movimientos_db) if m["id"] == movimiento_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    patch = {k: v for k, v in data.dict().items() if v is not None}
    movimientos_db[idx].update(patch)
    return movimientos_db[idx]

@app.delete("/movimientos/{movimiento_id}", response_model=dict, tags=["Movimientos"])
def delete_movimiento(movimiento_id: int):
    idx = next((i for i, m in enumerate(movimientos_db) if m["id"] == movimiento_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    deleted = movimientos_db.pop(idx)
    return {"mensaje": "Movimiento eliminado", "id": deleted["id"]}


# ─── Dashboard ────────────────────────────────────────────────────────────────

@app.get("/dashboard/metricas", tags=["Dashboard"])
def get_metricas():
    productos_activos = [p for p in productos_db if p["activo"]]
    stock_bajo = [p for p in productos_db if p["stock"] <= p["stock_minimo"]]
    valor_costo = sum(p["costo"] * p["stock"] for p in productos_db)
    valor_venta = sum(p["precio"] * p["stock"] for p in productos_db)
    proveedores_activos = [p for p in proveedores_db if p["activo"]]
    categorias_activas = [c for c in categorias_db if c["activa"]]
    entradas = [m for m in movimientos_db if m["tipo"] == "entrada"]
    salidas = [m for m in movimientos_db if m["tipo"] == "salida"]
    ajustes = [m for m in movimientos_db if m["tipo"] == "ajuste"]
    ultimos = sorted(movimientos_db, key=lambda m: m["fecha"], reverse=True)[:6]

    return {
        "total_productos": len(productos_db),
        "productos_activos": len(productos_activos),
        "productos_stock_bajo": len(stock_bajo),
        "lista_stock_bajo": sorted(stock_bajo, key=lambda p: p["stock"])[:5],
        "valor_inventario_costo": round(valor_costo, 2),
        "valor_inventario_venta": round(valor_venta, 2),
        "margen_potencial": round(valor_venta - valor_costo, 2),
        "total_proveedores_activos": len(proveedores_activos),
        "total_categorias_activas": len(categorias_activas),
        "total_movimientos": len(movimientos_db),
        "total_entradas": len(entradas),
        "total_salidas": len(salidas),
        "total_ajustes": len(ajustes),
        "unidades_ingresadas": sum(m["cantidad"] for m in entradas),
        "unidades_egresadas": sum(m["cantidad"] for m in salidas),
        "ultimos_movimientos": ultimos,
    }

@app.get("/dashboard/stock-por-categoria", tags=["Dashboard"])
def get_stock_por_categoria():
    resultado = []
    for cat in categorias_db:
        prods_cat = [p for p in productos_db if p["categoria_id"] == cat["id"]]
        total_stock = sum(p["stock"] for p in prods_cat)
        valor_cat = sum(p["costo"] * p["stock"] for p in prods_cat)
        resultado.append({
            "categoria_id": cat["id"],
            "categoria": cat["nombre"],
            "total_productos": len(prods_cat),
            "total_stock": total_stock,
            "valor_inventario": round(valor_cat, 2),
        })
    return resultado


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "version": "1.0.0"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)