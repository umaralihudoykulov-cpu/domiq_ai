"""Estimates - API Views"""
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Material prices (UZS per unit)
MATERIAL_PRICES = {
    'laminate': {'price': 45000, 'unit': 'm²', 'name': 'Laminat'},
    'tile': {'price': 65000, 'unit': 'm²', 'name': 'Kafel'},
    'paint': {'price': 8000, 'unit': 'm²', 'name': 'Bo\'yoq (2 qavat)'},
    'wallpaper': {'price': 25000, 'unit': 'm²', 'name': 'Oboi'},
    'plaster': {'price': 12000, 'unit': 'm²', 'name': 'Shpaklyovka'},
    'gypsum': {'price': 35000, 'unit': 'm²', 'name': 'Gipsokarton'},
    'cement': {'price': 4500, 'unit': 'kg', 'name': 'Sement'},
    'cable': {'price': 3500, 'unit': 'm', 'name': 'Elektr kabel'},
    'led': {'price': 12000, 'unit': 'm', 'name': 'LED lenta'},
    'profile': {'price': 8000, 'unit': 'm', 'name': 'Metall profil'},
}

# Labor costs (UZS per m²)
LABOR_COSTS = {
    'cosmetic': 150000,
    'euro': 350000,
    'design': 650000,
    'premium': 1200000,
    'full': 800000,
}


@login_required
@require_POST
def calculate_materials_api(request):
    """Calculate materials needed"""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST.dict()
    
    area = float(data.get('area', 50))
    rooms = int(data.get('rooms', 3))
    ceiling_height = float(data.get('ceiling_height', 2.7))
    
    # Calculate quantities
    floor_area = area
    wall_area = (area ** 0.5) * 4 * ceiling_height * 0.85  # approx
    ceiling_area = area
    
    calculations = []
    
    # Floor materials
    laminate_qty = floor_area * 1.1  # 10% waste
    calculations.append({
        'category': 'Pol',
        'name': 'Laminat (8mm)',
        'quantity': round(laminate_qty, 1),
        'unit': 'm²',
        'unit_price': MATERIAL_PRICES['laminate']['price'],
        'total': round(laminate_qty * MATERIAL_PRICES['laminate']['price']),
    })
    
    # Tile for bathroom
    bathroom_area = rooms * 6  # avg 6m² per bathroom
    tile_qty = bathroom_area * 1.15
    calculations.append({
        'category': 'Hammom',
        'name': 'Kafel',
        'quantity': round(tile_qty, 1),
        'unit': 'm²',
        'unit_price': MATERIAL_PRICES['tile']['price'],
        'total': round(tile_qty * MATERIAL_PRICES['tile']['price']),
    })
    
    # Paint for walls
    paint_area = wall_area - bathroom_area
    calculations.append({
        'category': 'Devor',
        'name': 'Devor bo\'yog\'i',
        'quantity': round(paint_area, 1),
        'unit': 'm²',
        'unit_price': MATERIAL_PRICES['paint']['price'],
        'total': round(paint_area * MATERIAL_PRICES['paint']['price']),
    })
    
    # Plaster
    calculations.append({
        'category': 'Devor',
        'name': 'Shpaklyovka',
        'quantity': round(wall_area, 1),
        'unit': 'm²',
        'unit_price': MATERIAL_PRICES['plaster']['price'],
        'total': round(wall_area * MATERIAL_PRICES['plaster']['price']),
    })
    
    # Gypsum ceiling
    gyp_qty = ceiling_area * 1.1
    calculations.append({
        'category': 'Shift',
        'name': 'Gipsokarton shift',
        'quantity': round(gyp_qty, 1),
        'unit': 'm²',
        'unit_price': MATERIAL_PRICES['gypsum']['price'],
        'total': round(gyp_qty * MATERIAL_PRICES['gypsum']['price']),
    })
    
    # Cable
    cable_length = area * 1.8
    calculations.append({
        'category': 'Elektr',
        'name': 'Elektr kabel (2.5mm²)',
        'quantity': round(cable_length, 1),
        'unit': 'm',
        'unit_price': MATERIAL_PRICES['cable']['price'],
        'total': round(cable_length * MATERIAL_PRICES['cable']['price']),
    })
    
    # LED strips
    led_length = (area ** 0.5) * 4
    calculations.append({
        'category': 'Yoritish',
        'name': 'LED lenta',
        'quantity': round(led_length, 1),
        'unit': 'm',
        'unit_price': MATERIAL_PRICES['led']['price'],
        'total': round(led_length * MATERIAL_PRICES['led']['price']),
    })
    
    total_cost = sum(item['total'] for item in calculations)
    
    return JsonResponse({
        'success': True,
        'area': area,
        'rooms': rooms,
        'calculations': calculations,
        'total_material_cost': total_cost,
        'formatted_total': f"{total_cost:,} so'm",
    })


@login_required
@require_POST
def calculate_estimate_api(request):
    """Full renovation estimate calculator"""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST.dict()
    
    area = float(data.get('area', 50))
    repair_type = data.get('repair_type', 'euro')
    rooms = int(data.get('rooms', 3))
    has_smart_home = data.get('has_smart_home', False)
    has_furniture = data.get('has_furniture', False)
    project_id = data.get('project_id')
    
    # Labor
    labor_per_m2 = LABOR_COSTS.get(repair_type, 350000)
    labor_cost = area * labor_per_m2
    
    # Materials (70% of labor typically)
    material_cost = labor_cost * 0.7
    
    # Electrical
    electrical_cost = area * 85000
    
    # Smart home
    smart_home_cost = (area * 150000) if has_smart_home else 0
    
    # Furniture
    furniture_cost = (area * 400000) if has_furniture else 0
    
    # Design
    design_cost = area * 50000 if repair_type in ['design', 'premium'] else 0
    
    total = labor_cost + material_cost + electrical_cost + smart_home_cost + furniture_cost + design_cost
    
    # Save to DB if project_id provided
    if project_id:
        try:
            from projects.models import Project
            from estimates.models import Estimate
            project = Project.objects.get(id=project_id, user=request.user)
            
            estimate = Estimate.objects.create(
                project=project,
                user=request.user,
                title=f"{project.title} - AI Smeta",
                labor_cost=labor_cost,
                material_cost=material_cost,
                electrical_cost=electrical_cost,
                smart_home_cost=smart_home_cost,
                furniture_cost=furniture_cost,
                design_cost=design_cost,
                ai_generated=True,
            )
        except Exception as e:
            # project topilmasa yoki xatolik yuz bersa, smeta baribir qaytariladi
            import logging
            logging.getLogger(__name__).warning(f"Estimate save error for project {project_id}: {e}")
    
    breakdown = [
        {'category': 'Ish haqi', 'cost': int(labor_cost), 'icon': '👷'},
        {'category': 'Materiallar', 'cost': int(material_cost), 'icon': '🧱'},
        {'category': 'Elektr montaj', 'cost': int(electrical_cost), 'icon': '⚡'},
    ]
    
    if smart_home_cost > 0:
        breakdown.append({'category': 'Smart Home', 'cost': int(smart_home_cost), 'icon': '🏠'})
    if furniture_cost > 0:
        breakdown.append({'category': 'Mebel', 'cost': int(furniture_cost), 'icon': '🛋️'})
    if design_cost > 0:
        breakdown.append({'category': 'Dizayn', 'cost': int(design_cost), 'icon': '🎨'})
    
    return JsonResponse({
        'success': True,
        'area': area,
        'repair_type': repair_type,
        'breakdown': breakdown,
        'total': int(total),
        'total_formatted': f"{int(total):,} so'm",
        'per_m2': int(total / area),
        'per_m2_formatted': f"{int(total/area):,} so'm/m²",
        'timeline_days': int(area * 1.2),
    })
