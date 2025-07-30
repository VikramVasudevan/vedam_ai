class VedamConfig:
    # shuklaYajurVedamPdfPath: str = "./data/shukla-yajur-veda.pdf"
    # shuklaYajurVedamSmallPdfPath: str = "./data/shukla-yajur-veda-small.pdf"
    # vishnuPuranamPdfPath = "./data/vishnu_puranam.pdf"
    # dbStorePath: str = "./chromadb-store"
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
            "language" : "san+eng"
        },
        {
            "name": "shukla_yajur_vedam",
            "title": "Shukla Yajur Vedam",
            "output_dir": "./output/shukla_yajur_vedam",
            "collection_name": "shukla_yajur_vedam",
            "pdf_path": "./data/shukla-yajur-veda.pdf",
            "language" : "san+eng"
        },
    ]
