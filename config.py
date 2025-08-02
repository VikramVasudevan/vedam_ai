class VedamConfig:
    # shuklaYajurVedamPdfPath: str = "./data/shukla-yajur-veda.pdf"
    # shuklaYajurVedamSmallPdfPath: str = "./data/shukla-yajur-veda-small.pdf"
    # vishnuPuranamPdfPath = "./data/vishnu_puranam.pdf"
    dbStorePath: str = "./chromadb-store"
    # shuklaYajurVedamCollectionName: str = "shukla_yajur_vedam"
    # vishnuPuranamCollectionName: str = "vishnu_puranam"
    # shuklaYajurVedamOutputDir = "./output/shukla_yajur_vedam"
    # vishnuPuranamOutputDir = "./output/vishnu_puranam"
    scriptures = [
        {
            "name": "vishnu_puranam",
            "title": "Sri Vishnu Puranam",
            "output_dir": "./output/vishnu_puranam",
            "collection_name": "vishnu_puranam",
            "pdf_path": "./data/vishnu_puranam.pdf",
            "language": "san+eng",
            "example_labels": [
                "Vishnu's form",
                "About the five elements",
                "About Garuda",
                "Weapons of Vishnu",
            ],
            "examples": [
                "describe Vishnu's form",
                "five elements and their significance",
                "What is the significance of Garuda? Show some verses that describe him.",
                "What weapons does Vishnu hold?",
            ]
        },
        {
            "name": "shukla_yajur_vedam",
            "title": "Shukla Yajur Vedam",
            "output_dir": "./output/shukla_yajur_vedam",
            "collection_name": "shukla_yajur_vedam",
            "pdf_path": "./data/shukla-yajur-veda.pdf",
            "language": "san+eng",
            "example_labels": [
                "About Vedam",
                "About the five elements",
                "About Brahma",
            ],
            "examples": [
                "Gist of Shukla Yajur Vedam. Give me some sanskrit verses.",
                "What is the significance of fire and water. show some sanskrit verses",
                "Brahma",
            ],
        },
        {
            "name": "bhagavat_gita",
            "title": "Bhagavat Gita",
            "output_dir": "./output/bhagavat_gita",
            "collection_name": "bhagavat_gita",
            "pdf_path": "./data/bhagavat_gita.pdf",
            "language": "san+eng",
            "example_labels": [
                "About Arjuna",
                "About Karma",
                "About birth and death",
                "About the battle field",
                "About Krishna's form"
            ],
            "examples": [
                "Show some verses where Krishna advises Arjuna",
                "What does Krishna say about Karma",
                "What does Krishna say about birth and death",
                "describe the battle field",
                "Vishwarupa"
            ],
        },
        {
            "name": "valmiki_ramayanam",
            "title": "Valmiki Ramayanam",
            "output_dir": "./output/valmiki_ramayanam",
            "collection_name": "valmiki_ramayanam",
            "pdf_path": "./data/valmiki_ramayanam.pdf",
            "language": "san+eng",
            "example_labels": [
                "About Jatayu",
                "About Hanuman",
                "About Vali",
                "About Sita",
                "About Ravana",
            ],
            "examples": [
                "What is the significance of Jatayu? show some sanskrit verses to support the argument",
                "Show some verses where Hanuman is mentioned",
                "How did Rama kill Vali",
                "How was Sita abducted",
                "How did Rama kill Ravana?",
            ],
        },
        {
            "name": "vishnu_sahasranamam",
            "title": "Vishnu Sahasranamam",
            "output_dir": "./output/vishnu_sahasranamam",
            "collection_name": "vishnu_sahasranamam",
            "pdf_path": "./data/vishnu_sahasranamam.pdf",
            "language": "san+eng",
            "example_labels": ["Vanamali", "1000 names", "Sanskrit text search"],
            "examples": [
                "Vanamali",
                "Show some of the 1000 names of Vishnu along with their meaning",
                "show the verse that begins with शुक्लाम्बरधरं",
            ],
        },
        {
            "name": "bhagavata_purana",
            "title": "Bhagavatha Puranam",
            "output_dir": "./output/bhagavata_purana",
            "collection_name": "bhagavata_purana",
            "pdf_path": "./data/bhagavata_purana.pdf",
            "language": "san+eng",
            "example_labels": [
                "Gajendra Moksham",
                "Prahalad"
            ],
            "examples": [
                "State some verses that showcase the devotion of Gajendra the elephant",
                "State some verses that showcase the devotion of Prahlada"
            ]
        },

    ]
