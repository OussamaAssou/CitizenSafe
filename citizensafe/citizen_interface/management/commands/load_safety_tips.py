from django.core.management.base import BaseCommand
from citizen_interface.models import SafetyTip

class Command(BaseCommand):
    help = 'Charge les conseils de sécurité dans la base de données'

    def handle(self, *args, **options):
        safety_tips = [
            {
                'title': 'Sécurisez vos portes et fenêtres',
                'content': 'Assurez-vous que toutes les portes et fenêtres sont bien verrouillées avant de quitter votre domicile ou d\'aller dormir.'
            },
            {
                'title': 'Éclairage extérieur',
                'content': 'Installez des lumières à détection de mouvement autour de votre maison pour dissuader les intrus.'
            },
            {
                'title': 'Système d\'alarme',
                'content': 'Envisagez l\'installation d\'un système d\'alarme et affichez clairement que votre maison est protégée.'
            },
            {
                'title': 'Connaissez vos voisins',
                'content': 'Établissez de bonnes relations avec vos voisins. Ils peuvent garder un œil sur votre propriété lorsque vous êtes absent.'
            },
            {
                'title': 'Ne partagez pas vos absences sur les réseaux sociaux',
                'content': 'Évitez d\'annoncer vos vacances ou absences prolongées sur les réseaux sociaux.'
            },
            {
                'title': 'Utilisez des minuteries pour les lumières',
                'content': 'Utilisez des minuteries pour allumer et éteindre les lumières à des heures variables lorsque vous êtes absent.'
            },
            {
                'title': 'Sécurisez votre Wi-Fi',
                'content': 'Utilisez un mot de passe fort pour votre réseau Wi-Fi et changez-le régulièrement.'
            },
            {
                'title': 'Gardez vos objets de valeur en sécurité',
                'content': 'Utilisez un coffre-fort pour ranger vos objets de valeur et documents importants.'
            },
            {
                'title': 'Entretenez votre jardin',
                'content': 'Un jardin bien entretenu donne l\'impression que la maison est occupée et surveillée.'
            },
            {
                'title': 'Soyez prudent avec les clés',
                'content': 'Ne cachez pas de clés à l\'extérieur de votre maison. Confiez plutôt un double à une personne de confiance.'
            },
            {
                'title': 'Installez des serrures de qualité',
                'content': 'Investissez dans des serrures de haute qualité pour vos portes et fenêtres.'
            },
            {
                'title': 'Sécurisez votre garage',
                'content': 'N\'oubliez pas de verrouiller la porte entre votre garage et votre maison.'
            },
            {
                'title': 'Attention aux démarcheurs',
                'content': 'Méfiez-vous des inconnus qui sonnent à votre porte. Vérifiez toujours leur identité.'
            },
            {
                'title': 'Signalez les activités suspectes',
                'content': 'N\'hésitez pas à signaler toute activité suspecte dans votre quartier à la police.'
            },
            {
                'title': 'Faites attention à vos clés de voiture',
                'content': 'Ne laissez jamais vos clés de voiture dans votre véhicule, même dans votre garage.'
            },
        ]

        for tip in safety_tips:
            SafetyTip.objects.create(title=tip['title'], content=tip['content'])

        self.stdout.write(self.style.SUCCESS('Conseils de sécurité chargés avec succès'))