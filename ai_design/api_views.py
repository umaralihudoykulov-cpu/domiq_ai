"""AI Design - API Views with OpenAI"""
import json
import time
import os
import base64
import uuid
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import AIDesign, AIChat, AIChatMessage
import openai

# Design styles configuration
DESIGN_STYLES = {
    'modern': 'Modern minimalist design with clean lines, neutral colors, and functional furniture',
    'minimal': 'Ultra minimalist design with white space, simple forms, and monochromatic palette',
    'scandinavian': 'Scandinavian design with light woods, whites, natural textures, cozy atmosphere',
    'loft': 'Industrial loft style with exposed brick, concrete, metal accents, open spaces',
    'classic': 'Classic elegant design with ornate details, rich fabrics, warm colors',
    'japandi': 'Japanese-Scandinavian fusion with zen minimalism, natural materials, muted tones',
    'luxury': 'Ultra luxury design with marble, gold accents, premium materials, opulent details',
    'neo_classic': 'Neo-classical modern with symmetry, architectural details, sophisticated palette',
}

ROOM_TYPES = {
    'living_room': 'living room',
    'bedroom': 'bedroom',
    'kitchen': 'modern kitchen',
    'bathroom': 'luxury bathroom',
    'office': 'home office',
    'dining': 'dining room',
    'hallway': 'elegant hallway',
}


def build_design_prompt(room_type, style, area, color_scheme, budget_level, custom=''):
    room = ROOM_TYPES.get(room_type, 'room')
    style_desc = DESIGN_STYLES.get(style, 'modern design')
    budget_note = {'low': 'budget-friendly', 'medium': 'mid-range', 'high': 'high-end', 'luxury': 'ultra-luxury'}.get(budget_level, 'quality')
    
    prompt = f"""Ultra-realistic interior design render of a {room}, {area} square meters.
Style: {style_desc}.
Color scheme: {color_scheme}.
Budget level: {budget_note}.
Features: professional lighting with hidden LED strips, premium furniture placement,
architectural visualization quality, 8K render, photorealistic, cinematic lighting,
natural light from windows, perfect composition, architectural digest quality.
{custom}
--no text, no watermarks, no people"""
    return prompt


@login_required
@require_POST
def generate_design_api(request):
    """Generate AI interior design"""
    user = request.user
    
    if not user.can_use_ai:
        return JsonResponse({
            'error': f"Kunlik limit tugadi! {user.plan} plan: {user.ai_limit} ta so'rov/kun. Premium rejaga o'ting.",
            'upgrade_url': '/pricing/'
        }, status=429)
    
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST
    
    room_type = data.get('room_type', 'living_room')
    style = data.get('style', 'modern')
    area = float(data.get('area', 30))
    color_scheme = data.get('color_scheme', 'neutral warm tones')
    budget_level = data.get('budget_level', 'medium')
    custom_prompt = data.get('custom_prompt', '')
    project_id = data.get('project_id')
    
    # Build prompt
    prompt = build_design_prompt(room_type, style, area, color_scheme, budget_level, custom_prompt)
    
    start_time = time.time()
    
    # Create DB record
    design = AIDesign.objects.create(
        user=user,
        room_type=room_type,
        style=style,
        area=area,
        color_scheme=color_scheme,
        budget_level=budget_level,
        custom_prompt=custom_prompt,
        prompt_used=prompt,
        status='processing',
    )
    
    if project_id:
        try:
            from projects.models import Project
            project = Project.objects.get(id=project_id, user=user)
            design.project = project
            design.save(update_fields=['project'])
        except Exception:
            pass  # project_id noto'g'ri yoki ruxsat yo'q — davom etamiz
    
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    # Demo mode if no API key
    if not api_key or api_key == 'your-openai-api-key-here':
        import random
        demo_images = [
            'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=1024&q=80',
            'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=1024&q=80',
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=1024&q=80',
            'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=1024&q=80',
        ]
        image_url = random.choice(demo_images)
        design.image_url = image_url
        design.status = 'completed'
        design.generation_time = time.time() - start_time
        design.ai_response = f"Demo rejim: {style.title()} stil {room_type} dizayni."
        design.color_palette = ['#F5F0EB', '#2D2926', '#8B7355', '#E8DDD0', '#4A90D9']
        design.furniture_suggestions = ['Zamonaviy divan', 'Marmar stolcha', 'LED yoritgichlar']
        design.save()
        # Faqat counter maydonlarni yangilash (race condition oldini olish)
        from django.db.models import F
        type(user).objects.filter(pk=user.pk).update(
            ai_requests_today=F('ai_requests_today') + 1,
            ai_requests_total=F('ai_requests_total') + 1,
        )
        user.refresh_from_db(fields=['ai_requests_today', 'ai_requests_total'])
        return JsonResponse({'success': True, 'design_id': design.id, 'image_url': image_url,
            'style': style, 'ai_response': design.ai_response,
            'color_palette': design.color_palette, 'demo_mode': True})
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # gpt-image-1 — haqiqiy AI render
        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality="high",
            n=1,
        )
        
        # gpt-image-1 returns base64 — save to media (MEDIA_ROOT dan foydalanish)
        b64_data = image_response.data[0].b64_json
        img_bytes = base64.b64decode(b64_data)
        
        media_dir = Path(settings.MEDIA_ROOT) / 'ai_designs'
        media_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        (media_dir / filename).write_bytes(img_bytes)
        image_url = f"{settings.MEDIA_URL}ai_designs/{filename}"
        
        # GPT-4o description in Uzbek
        chat_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Siz professional interior dizayner sifatida O'zbek tilida qisqa tavsiflar yozasiz."},
                {"role": "user", "content": f"{style} stilida {room_type} dizayni ({area} m², {color_scheme}). O'zbek tilida qisqacha tavsif va 5 ta mebel tavsiyasi bering."}
            ],
            max_tokens=600,
        )
        
        ai_text = chat_response.choices[0].message.content
        
        design.image_url = image_url
        design.status = 'completed'
        design.generation_time = time.time() - start_time
        design.ai_response = ai_text
        design.color_palette = ['#F5F0EB', '#2D2926', '#8B7355', '#E8DDD0', '#4A90D9']
        design.save()
        
        # Faqat counter maydonlarni yangilash (race condition oldini olish)
        from django.db.models import F
        type(user).objects.filter(pk=user.pk).update(
            ai_requests_today=F('ai_requests_today') + 1,
            ai_requests_total=F('ai_requests_total') + 1,
        )
        user.refresh_from_db(fields=['ai_requests_today', 'ai_requests_total'])
        
        return JsonResponse({
            'success': True,
            'design_id': design.id,
            'image_url': image_url,
            'style': style,
            'ai_response': ai_text,
            'color_palette': design.color_palette,
            'generation_time': round(design.generation_time, 1),
            'demo_mode': False,
        })
        
    except Exception as e:
        design.status = 'failed'
        design.save()
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def ai_chat_api(request):
    """AI Chat Consultant"""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST
    
    message = data.get('message', '').strip()
    session_id = data.get('session_id', f"session_{request.user.id}")
    
    if not message:
        return JsonResponse({'error': 'Xabar bo\'sh'}, status=400)
    
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    SYSTEM_PROMPT = """Siz DomIQ Pro Max platformasining AI dizayn konsultantisinz. 
Uzbek tilida professional va do'stona muloqot qilasiz.
Siz uy dizayni, remont, elektr montaj, materiallar, narxlar va qurilish bo'yicha mutaxassissinz.
Har doim aniq, foydali va amaliy maslahatlar bering.
Narxlarni so'm (UZS) da ko'rsating."""
    
    if not api_key or api_key == 'your-openai-api-key-here':
        # Demo responses
        demo_responses = {
            'salom': 'Salom! Men DomIQ AI konsultantiman. Uy dizayni, remont yoki materiallar haqida savollaringiz bormi? 😊',
            'narx': 'Evro remont narxi odatda 1 kv.m uchun 800,000 - 2,000,000 so\'m atrofida. Bu materiallar va ishchilar xarajatlarini o\'z ichiga oladi.',
            'dizayn': 'Zamonaviy dizayn uchun Scandinavian yoki Japandi stilini tavsiya qilaman - soddalik va funktsionallik uyg\'unligini ta\'minlaydi.',
        }
        
        response_text = "Men demo rejimda ishlayapman. OpenAI API kaliti kiritilganda to'liq imkoniyatlardan foydalanishingiz mumkin. Uy dizayni, remont narxlari va materiallar bo'yicha savollaringizga javob berishga tayyorman! 🏠"
        
        for key, val in demo_responses.items():
            if key in message.lower():
                response_text = val
                break
        
        return JsonResponse({'success': True, 'response': response_text, 'demo': True})
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Get chat history
        chat, _ = AIChat.objects.get_or_create(
            user=request.user,
            session_id=session_id,
        )
        
        history = list(chat.messages.order_by('-created_at')[:10])
        history.reverse()
        
        messages_list = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in history:
            messages_list.append({"role": msg.role, "content": msg.content})
        messages_list.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_list,
            max_tokens=1000,
        )
        
        ai_response = response.choices[0].message.content
        
        # Save messages
        AIChatMessage.objects.create(chat=chat, role='user', content=message)
        AIChatMessage.objects.create(chat=chat, role='assistant', content=ai_response)
        
        return JsonResponse({'success': True, 'response': ai_response})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required  
@require_POST
def electrical_analyze_api(request):
    """Analyze floor plan for electrical planning"""
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    area = float(request.POST.get('area', 50))
    rooms = int(request.POST.get('rooms', 3))
    has_smart = request.POST.get('has_smart_home', 'false') == 'true'
    
    if not api_key or api_key == 'your-openai-api-key-here':
        # Demo electrical plan
        sockets = int(area * 0.6)
        lights = int(rooms * 3)
        cable = round(area * 1.8, 1)
        
        result = {
            'success': True,
            'demo': True,
            'sockets': sockets,
            'switches': rooms * 2,
            'lights': lights,
            'cable_length': cable,
            'circuit_breakers': max(6, rooms + 2),
            'estimated_cost': int(area * 85000),
            'recommendations': [
                f'Jami {sockets} ta rozetka o\'rnatish tavsiya etiladi',
                f'Har bir xonaga kamida 3 ta yoritgich',
                f'Kabel uzunligi: taxminan {cable} metr',
                'Smart-home uchun 220V va 12V liniyalar alohida o\'tkazilsin' if has_smart else 'UZO himoya qurilmalari o\'rnatilsin',
                'Asosiy щit 3-fazali 25A bo\'lishi kerak',
                'Elektr plita uchun alohida 32A liniya',
            ],
            'analysis': f'{area} kv.m {rooms} xonali uy uchun professional elektr reja tayyor. Barcha rozetka va chiroqlar GOST standartiga mos joylashtirilgan.'
        }
        return JsonResponse(result)
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        image_file = request.FILES.get('floor_plan')
        
        prompt = f"""Siz professional elektr muhandisisinz. {area} kv.m, {rooms} xonali uy uchun elektr montaj rejasini tuzing.
{'Smart-home integratsiyasi kiritilsin.' if has_smart else ''}

Quyidagilarni JSON formatda bering:
{{
  "sockets": <rozetka soni>,
  "switches": <kalid soni>,
  "lights": <chiroq soni>,
  "cable_length": <kabel uzunligi metr>,
  "circuit_breakers": <avtomat soni>,
  "estimated_cost": <taxminiy narx so\'mda>,
  "recommendations": [<5-7 ta tavsiya>,],
  "analysis": "<qisqacha tahlil>"
}}"""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=1000,
        )
        
        result = json.loads(response.choices[0].message.content)
        result['success'] = True
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
