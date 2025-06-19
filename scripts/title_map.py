# scripts/title_map.py

TITLE_MAP = {
    # Units & Distances
    "Light year, parsec, astronomical unit": "Units of astronomical distance",

    # Electromagnetic & Telescopes
    "Electromagnetic spectrum in astronomy": "Electromagnetic spectrum",
    "Telescopes: optical, radio, space-based": "Telescope",

    # Solar System
    "Planets in the solar system": "Solar System",
    "Moons of the planets": "Natural satellite",
    "Dwarf planets (e.g. Pluto)": "Dwarf planet",
    "Asteroids vs comets vs meteoroids": "Asteroid",
    "The asteroid belt": "Asteroid belt",
    "The Kuiper Belt and Oort Cloud": "Kuiper belt",

    # Earth Motions
    "Earth's rotation and revolution": "Earth's rotation",
    "Seasons and equinoxes": "Axial tilt",
    "Solar and lunar eclipses": "Eclipse",
    "Tides and moon's gravity": "Tide",

    # Stars
    "What is a star?": "Star",
    "Life cycle of stars": "Stellar evolution",
    "Stellar classification (OBAFGKM)": "Stellar classification",
    "Nuclear fusion in stars": "Nuclear fusion",
    "Supernova and hypernova": "Supernova",
    "Red giants and supergiants": "Red giant",
    "Black dwarfs": "Black dwarf",
    "Binary and variable stars": "Variable star",

    # Black Holes & Exotic
    "Black holes (stellar, supermassive, primordial)": "Black hole",
    "Event horizon and singularity": "Event horizon",
    "Quasars and blazars": "Quasar",
    "Pulsars and magnetars": "Pulsar",
    "Dark matter and dark energy": "Dark matter",
    "Cosmic strings and multiverse theories": "Cosmic string",

    # Galaxies & Structures
    "What is a galaxy?": "Galaxy",
    "Cosmic web structure": "Large-scale structure of the cosmos",

    # Space Exploration
    "Voyager 1 and 2": "Voyager program",
    "NASA, ESA, ISRO, Roscosmos overview": "Space agency",

    # Pop Sci Questions
    "What is the universe?": "Universe",
    "What is the Big Bang?": "Big Bang",
    "What is a black hole?": "Black hole",
    "What is the Observable Universe?": "Observable universe",
    "What is the Cosmic Microwave Background?": "Cosmic microwave background",
    "What is the Cosmic Horizon?": "Cosmic horizon",
    "What is the Cosmic Web?": "Large-scale structure of the cosmos",
    "Can black holes be used for time travel?": "Time travel",
    "Why can't we see stars in space photos?": "Hubble Deep Field",
    "Can you hear sound in space?": "Sound in space",
    "Is hyperspace possible?": "Hyperspace (science fiction)",
    "What are Dyson spheres?": "Dyson sphere",
    "What is the Great Filter?": "Great Filter",
    "What is the Kardashev scale?": "Kardashev scale",
    "What is the Anthropic Principle?": "Anthropic principle",
}


def resolve_title(topic: str) -> str:
    """Returns the mapped Wikipedia title if available."""
    return TITLE_MAP.get(topic.strip(), topic.strip().title())
