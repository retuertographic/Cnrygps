# -*- coding: utf-8 -*-
"""Datos y textos de Canary GPS (ES / EN).

Todo el contenido procede de la web original de Canary GPS. Cada texto es un
par (español, inglés); `generar.py` elige el idioma al componer cada página.
"""

EMPRESA = {
    'nombre': 'Canary GPS',
    'email': 'hola@canarygps.com',
    'telefono': '+34 000 000 000',          # pendiente: teléfono definitivo
    'telefono_href': '+34000000000',
    'zona': ('Tenerife, Canarias', 'Tenerife, Canary Islands'),
    'pagos': 'https://pagos.canarygps.com/pagar.php',
    'base_url': 'https://canarygps.com/',
}

IMG = {
    'vehiculo': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?q=75&w=1600&auto=format&fit=crop',
    'mascotas': 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?q=75&w=1600&auto=format&fit=crop',
    'flotas': 'https://images.unsplash.com/photo-1519003722824-194d4455a60c?q=75&w=1600&auto=format&fit=crop',
    'publicidad': 'https://images.unsplash.com/photo-1600661653561-629509216228?q=75&w=1600&auto=format&fit=crop',
    'hogar': 'https://images.unsplash.com/photo-1558002038-1055907df827?q=75&w=1600&auto=format&fit=crop',
}

# ---------------------------------------------------------------- Planes
PLANES = [
    # clave, nombre, precio/mes, total, descuento
    ('mensual', ('Mensual', 'Monthly'), '5,00 €', ('5,00 € cada mes', '€5.00 every month'), None),
    ('trimestral', ('Trimestral', 'Quarterly'), '4,50 €', ('13,50 € cada 3 meses', '€13.50 every 3 months'), '-10%'),
    ('semestral', ('Semestral', 'Six-monthly'), '4,00 €', ('24,00 € cada 6 meses', '€24.00 every 6 months'), '-20%'),
    ('anual', ('Anual', 'Annual'), '3,50 €', ('42,00 € al año', '€42.00 a year'), '-30%'),
]
PRECIO_EN = {'5,00 €': '€5.00', '4,50 €': '€4.50', '4,00 €': '€4.00', '3,50 €': '€3.50'}

# ---------------------------------------------------------------- Pasos
PASOS = [
    (('Recibe el dispositivo', 'Receive the device'),
     ('Te llega ya activado en tu cuenta. Abres la caja y está listo para usar.',
      'It arrives already activated on your account. Open the box and it is ready to use.')),
    (('Colócalo', 'Put it in place'),
     ('Imanes bajo el chasis, en el collar o junto a la puerta. Sin herramientas.',
      'Magnets under the chassis, on the collar or next to the door. No tools needed.')),
    (('Activa tu plan', 'Activate your plan'),
     ('Mensual, trimestral, semestral o anual. Puedes cambiarlo cuando quieras.',
      'Monthly, quarterly, six-monthly or annual. You can change it whenever you like.')),
    (('Controla todo desde la app', 'Control everything from the app'),
     ('Ubicación en tiempo real, historial de rutas y avisos de movimiento.',
      'Real-time location, route history and movement alerts.')),
]

DISPOSITIVO = [
    ('bateria', ('Hasta 240 días de batería', 'Up to 240 days of battery')),
    ('iman', ('Imanes, sin instalación', 'Magnets, no installation')),
    ('agua', ('Resistente a agua y polvo', 'Water and dust resistant')),
    ('aviso', ('Aviso de movimiento', 'Movement alert')),
]

FAQ_GENERAL = [
    (('¿Necesito wifi o electricidad del vehículo?', 'Do I need wifi or the vehicle’s power?'),
     ('No. Funciona con su propia batería y con datos móviles, así que sigue avisando aunque corten la luz o el internet del lugar donde está.',
      'No. It runs on its own battery and mobile data, so it keeps alerting you even if the power or internet is cut where it is.')),
    (('¿Puedo cambiar de plan cuando quiera?', 'Can I change plan whenever I want?'),
     ('Sí, puedes cambiar la duración de tu suscripción en cualquier momento desde tu cuenta.',
      'Yes, you can change the length of your subscription at any time from your account.')),
    (('¿Qué pasa si cancelo la suscripción?', 'What happens if I cancel my subscription?'),
     ('El dispositivo deja de reportar ubicación hasta que reactives el plan. No pierdes el aparato, solo el acceso a la plataforma mientras esté inactivo.',
      'The device stops reporting its location until you reactivate the plan. You keep the device; you only lose access to the platform while it is inactive.')),
    (('¿En cuánto tiempo lo localizo si se mueve?', 'How quickly can I locate it if it moves?'),
     ('La app te avisa al instante en cuanto detecta movimiento o desprendimiento, y puedes ver la ubicación en tiempo real desde ese momento.',
      'The app alerts you instantly as soon as it detects movement or removal, and you can see the location in real time from that moment.')),
]

# ---------------------------------------------------------------- Soluciones
SOLUCIONES = [
    {
        'slug': 'solucion-vehiculo', 'img': 'vehiculo', 'ico': 'coche',
        'nombre': ('Vehículo', 'Vehicle'),
        'antetitulo': ('Antirrobo y seguimiento', 'Anti-theft and tracking'),
        'titulo': ('No evitamos que lo intenten. Evitamos que se lo lleven.',
                   'We can’t stop them trying. We stop them getting away with it.'),
        'resumen': ('Localiza tu coche, furgoneta o vehículo camperizado en cualquier momento, sin depender de una instalación complicada.',
                    'Locate your car, van or campervan at any time, without relying on a complicated installation.'),
        'problema': ('Aparcar en la calle y no saber si tu vehículo seguirá allí al día siguiente es una preocupación real, sobre todo si lleva equipamiento de valor como una caseta de techo o material de trabajo.',
                     'Parking on the street without knowing whether your vehicle will still be there the next day is a real worry, especially if it carries valuable equipment such as a roof tent or work tools.'),
        'pasos': [
            (('Colócalo bajo el chasis', 'Place it under the chassis'),
             ('Se fija con imanes en minutos, sin cables ni visita técnica.', 'It attaches with magnets in minutes, with no cables or technician visit.')),
            (('Recibe avisos de movimiento', 'Get movement alerts'),
             ('Si el vehículo se mueve o alguien manipula el dispositivo, te enteras al instante.', 'If the vehicle moves or someone tampers with the device, you know instantly.')),
            (('Sigue la ubicación en vivo', 'Follow the live location'),
             ('Desde la app, en tiempo real, con historial de rutas de hasta 6 meses.', 'From the app, in real time, with up to 6 months of route history.')),
        ],
        'cta': ('¿Aparcas en la calle y quieres tranquilidad?', 'Park on the street and want peace of mind?'),
        'cta_btn': 'planes',
    },
    {
        'slug': 'solucion-mascotas', 'img': 'mascotas', 'ico': 'huella',
        'nombre': ('Mascotas', 'Pets'),
        'antetitulo': ('Localización de mascotas', 'Pet tracking'),
        'titulo': ('Que se escape no significa que se pierda.', 'Running off doesn’t mean getting lost.'),
        'resumen': ('Un susto de un segundo no tiene por qué convertirse en una noche entera buscando a tu mascota.',
                    'A one-second scare doesn’t have to turn into a whole night searching for your pet.'),
        'problema': ('Un ruido fuerte, una puerta abierta un segundo de más, y tu mascota ya no está donde la dejaste. Antes eso significaba carteles y horas de búsqueda.',
                     'A loud noise, a door left open a second too long, and your pet is no longer where you left it. That used to mean posters and hours of searching.'),
        'pasos': [
            (('Colócalo en el collar', 'Fit it to the collar'),
             ('Ligero y resistente al agua, pensado para llevarse puesto.', 'Light and water resistant, designed to be worn.')),
            (('Recibe un aviso al instante', 'Get an instant alert'),
             ('En cuanto se aleja de la zona habitual, te enteras en el móvil.', 'As soon as it leaves its usual area, you find out on your phone.')),
            (('Encuéntrala en minutos', 'Find it in minutes'),
             ('Ubicación en tiempo real desde la app, sin depender de que alguien la vea pasar.', 'Real-time location from the app, without relying on someone seeing it go by.')),
        ],
        'cta': ('¿Quieres tener siempre localizada a tu mascota?', 'Want to always know where your pet is?'),
        'cta_btn': 'planes',
    },
    {
        'slug': 'solucion-flotas', 'img': 'flotas', 'ico': 'camion',
        'nombre': ('Flotas', 'Fleets'),
        'antetitulo': ('Para negocios con varios vehículos', 'For businesses with several vehicles'),
        'titulo': ('Tu flota, de un vistazo.', 'Your fleet, at a glance.'),
        'resumen': ('Alquiler, reparto, tours o transporte. Ve dónde está cada vehículo, sin llamar a nadie para preguntarlo.',
                    'Rental, delivery, tours or transport. See where every vehicle is without having to call anyone to ask.'),
        'problema': ('Cada devolución tardía, cada desvío de ruta, cada cliente que pregunta «¿dónde está mi coche?» — antes era una llamada o una sorpresa en la factura de combustible. Con Canary GPS lo ves antes de que se convierta en un problema.',
                     'Every late return, every route detour, every customer asking “where’s my car?” used to mean a phone call or a surprise on the fuel bill. With Canary GPS you see it before it becomes a problem.'),
        'pasos': [
            (('Un GPS por vehículo', 'One GPS per vehicle'),
             ('Cada coche, furgoneta o embarcación de tu flota lleva su propio dispositivo, colocado en minutos.', 'Every car, van or boat in your fleet carries its own device, fitted in minutes.')),
            (('Un panel para todos', 'One dashboard for all'),
             ('Desde una sola cuenta ves la ubicación y el estado de todos tus vehículos a la vez.', 'From a single account you see the location and status of all your vehicles at once.')),
            (('Avisos automáticos', 'Automatic alerts'),
             ('Recibe una notificación si un vehículo se desvía de su ruta habitual o hay movimiento fuera de horario.', 'Get a notification if a vehicle strays from its usual route or moves outside working hours.')),
        ],
        'para': (('Pensado para', 'Designed for'), [
            (('Alquiler de vehículos', 'Vehicle rental'), ('Sabe si un coche llega tarde a su entrega antes de que te llame el cliente.', 'Know whether a car will be late for its handover before the customer calls you.')),
            (('Reparto y logística', 'Delivery and logistics'), ('Controla tiempos de ruta reales, no estimados.', 'Track real route times, not estimates.')),
            (('Tours y excursiones', 'Tours and excursions'), ('Verifica que cada vehículo sigue el recorrido previsto.', 'Check that every vehicle follows the planned route.')),
        ]),
        'faq': [
            (('¿Necesito un plan distinto por cada vehículo?', 'Do I need a separate plan for each vehicle?'),
             ('Cada GPS lleva su propia suscripción, pero puedes gestionarlas todas desde una única cuenta.', 'Each GPS has its own subscription, but you can manage them all from a single account.')),
            (('¿Puedo ver el historial de rutas de cada vehículo?', 'Can I see the route history of each vehicle?'),
             ('Sí, hasta 6 meses de historial por dispositivo.', 'Yes, up to 6 months of history per device.')),
        ],
        'cta': ('¿Cuántos vehículos tiene tu flota?', 'How many vehicles are in your fleet?'),
        'cta_btn': 'contacto',
    },
    {
        'slug': 'solucion-publicidad-en-movimiento', 'img': 'publicidad', 'ico': 'megafono',
        'nombre': ('Publicidad en movimiento', 'Advertising on the move'),
        'antetitulo': ('Para agencias y anunciantes', 'For agencies and advertisers'),
        'titulo': ('Marca en movimiento, no marca colgada en una pared.', 'A brand on the move, not a brand hanging on a wall.'),
        'resumen': ('Rotula vehículos reales en circulación y recibe la prueba de que tu inversión se movió por toda la isla, no solo la promesa.',
                    'Wrap real vehicles already on the road and get proof that your investment travelled all over the island, not just the promise.'),
        'problema': ('Mide el recorrido real de tu inversión publicitaria en vehículos, con informes periódicos.',
                     'Measure the real mileage of your vehicle advertising investment, with regular reports.'),
        'pasos': [
            (('Tu marca se rotula en vehículos ya en circulación', 'Your brand goes on vehicles already on the road'),
             ('Tours turísticos, reparto, flotas comerciales — vehículos que ya se mueven por la isla todos los días.', 'Tourist tours, delivery, commercial fleets: vehicles that already move around the island every day.')),
            (('Los vehículos siguen su actividad normal', 'Vehicles carry on as normal'),
             ('No cambia nada en su operativa. El GPS solo registra el recorrido, no interfiere en nada.', 'Nothing changes in how they operate. The GPS only records the route and does not interfere with anything.')),
            (('Recibes un informe periódico', 'You get a regular report'),
             ('Kilómetros recorridos, rutas, zonas de mayor tránsito y días activos, por vehículo, con la periodicidad que acordemos contigo.', 'Kilometres covered, routes, busiest areas and active days, per vehicle, as often as we agree with you.')),
        ],
        'nota': (('Sin ubicación en tiempo real', 'No real-time location'),
                 ('Solo compartimos informes agregados de recorrido, siempre con la autorización expresa del operador de la flota, cumpliendo con la normativa de protección de datos vigente.',
                  'We only share aggregated route reports, always with the express authorisation of the fleet operator and in compliance with current data protection law.')),
        'cta': ('¿Quieres ver cómo se movió tu marca este mes?', 'Want to see how your brand moved this month?'),
        'cta_btn': 'campana',
    },
    {
        'slug': 'solucion-hogar-y-negocio', 'img': 'hogar', 'ico': 'casa',
        'nombre': ('Hogar y negocio', 'Home and business'),
        'antetitulo': ('Seguridad sin depender de nada', 'Security that depends on nothing'),
        'titulo': ('Sigue avisando aunque corten la luz o el internet.', 'It keeps alerting you even if the power or internet is cut.'),
        'resumen': ('Lo primero que hace alguien que quiere entrar sin que te enteres es cortar la corriente. Con Canary GPS, eso ya no le sirve de nada.',
                    'The first thing someone does to get in without you knowing is cut the power. With Canary GPS, that no longer helps them.'),
        'problema': ('Las alarmas tradicionales dependen de la electricidad y del wifi del local. Canary GPS lleva su propia batería y se conecta por red móvil, así que sigue funcionando aunque fallen ambas cosas.',
                     'Traditional alarms depend on the premises’ electricity and wifi. Canary GPS has its own battery and connects over the mobile network, so it keeps working even if both fail.'),
        'pasos': [
            (('Colócalo en la puerta o ventana', 'Place it on the door or window'),
             ('Se fija con imanes en el marco o en la propia hoja, sin instalación ni cables.', 'It attaches with magnets to the frame or the door itself, with no installation or cables.')),
            (('Se activa con el movimiento', 'It activates with movement'),
             ('Si la puerta o ventana se abre, el dispositivo lo detecta al instante.', 'If the door or window opens, the device detects it instantly.')),
            (('Te avisa donde estés', 'It alerts you wherever you are'),
             ('Recibes la notificación en tu móvil, llegue de donde llegue, sin pasar por el wifi del local.', 'You get the notification on your phone, wherever you are, without going through the premises’ wifi.')),
        ],
        'para': (('Ideal para', 'Ideal for'), [
            (('Negocios y locales', 'Shops and business premises'), ('Una capa de aviso adicional, sobre todo fuera de horario.', 'An extra layer of alerts, especially outside opening hours.')),
            (('Obras y almacenes', 'Building sites and warehouses'), ('Sitios sin instalación eléctrica fija donde una alarma tradicional no es viable.', 'Places without a fixed electrical supply where a traditional alarm is not viable.')),
            (('Segundas residencias', 'Second homes'), ('Avisa aunque no tengas internet contratado en la vivienda.', 'It alerts you even if the property has no internet contract.')),
        ]),
        'nota': (('Un apunte honesto', 'An honest note'),
                 ('Es un aviso por movimiento del propio dispositivo, no un sensor de contacto magnético dedicado como las alarmas tradicionales. Es una capa adicional de aviso — no sustituye una alarma profesional si ya tienes una instalada.',
                  'It is an alert based on the device’s own movement, not a dedicated magnetic contact sensor like traditional alarms. It is an extra layer of warning and does not replace a professional alarm if you already have one installed.')),
        'cta': ('¿Tienes un negocio o local que proteger?', 'Do you have a business or premises to protect?'),
        'cta_btn': 'planes',
    },
]

VALORES = [
    (('Cercanía real', 'Real closeness'),
     ('No eres un número de ticket. Si tienes un problema, hablas con alguien que lo entiende.',
      'You are not a ticket number. If you have a problem, you talk to someone who understands it.')),
    (('Sin letra pequeña', 'No small print'),
     ('Los precios y las condiciones están claros desde el principio, en la web y en la factura.',
      'Prices and conditions are clear from the start, on the website and on the invoice.')),
    (('Seguridad sin alarmismo', 'Security without alarmism'),
     ('No vendemos miedo. Vendemos tranquilidad.', 'We don’t sell fear. We sell peace of mind.')),
]

HISTORIA = [
    ('Canary GPS nace de un miedo muy concreto: el de aparcar en la calle una furgoneta camperizada, con su caseta de techo, y no saber si seguiría allí al día siguiente. Empecé a buscar una forma de tener controlado el vehículo sin depender de una instalación complicada, y encontré en el GPS la solución.',
     'Canary GPS was born from a very specific fear: parking a campervan with its roof tent on the street and not knowing whether it would still be there the next day. I started looking for a way to keep an eye on the vehicle without relying on a complicated installation, and found the answer in GPS.'),
    ('Cuanto más compartía esa experiencia, más gente se interesaba — y no solo por el mismo motivo. Cada persona con la que hablaba me contaba un uso distinto: quien quería localizar a su perro, quien gestionaba varios vehículos de un negocio y no daba abasto controlándolos, quien necesitaba un aviso en un local sin instalación eléctrica fiable.',
     'The more I shared that experience, the more people became interested, and not only for the same reason. Everyone I spoke to told me about a different use: someone who wanted to locate their dog, someone who ran several business vehicles and couldn’t keep track of them all, someone who needed an alert in premises without a reliable electrical supply.'),
    ('De una necesidad personal salió un proyecto para cubrir todas esas necesidades, aquí, en Canarias.',
     'A personal need grew into a project to meet all of those needs, here in the Canary Islands.'),
]
