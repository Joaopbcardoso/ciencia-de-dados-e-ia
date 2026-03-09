import scrapy
import w3lib.html
import re


class ArrozGiassiSpider(scrapy.Spider):
    name = "arroz_giassi"
    
    # URLs iniciais - páginas de arroz (você pode adicionar mais páginas)
    start_urls = [
        "https://www.giassi.com.br/mercearia/alimentos-basicos/arroz?page=1",
        "https://www.giassi.com.br/mercearia/alimentos-basicos/arroz?page=2",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={'playwright': True})

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("BOT_NAME", "GiassiArrozBot", priority="spider")
        settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        # IMPORTANTE: Delay para não sobrecarregar o servidor
        settings.set("DOWNLOAD_DELAY", 2, priority="spider")

    def parse(self, response: scrapy.http.Response):
        """
        Extrai lista de produtos da página de categoria
        """
        # O Giassi usa VTEX - os produtos geralmente estão em containers específicos
        # Você precisa inspecionar o HTML real, mas aqui estão os seletores comuns:
        
        # Seletor para cada card de produto (ajuste conforme inspeção real)
        produtos = response.xpath('//div[contains(@class, "vtex-search-result-3-x-galleryItem")]')
        
        # Alternativa se a classe acima não funcionar:
        # produtos = response.css('div.vtex-product-summary-2-x-container')
        
        print(f'Encontrados {len(produtos)} produtos na página')
        
        for produto in produtos:
            # Extrair nome do produto
            nome = produto.xpath('.//h3//text() | .//h2//text() | .//span[contains(@class,"productBrand")]//text()').get()
            
            # Extrair link do produto
            link = produto.xpath('.//a[contains(@class,"vtex-product-summary-2-x-clearLink")]/@href | .//a/@href').get()
            if link and not link.startswith('http'):
                link = response.urljoin(link)
            
            # Extrair preço (pode estar escondido antes do login, mas tentamos)
            preco = produto.xpath('.//span[contains(@class,"sellingPrice")]//text() | .//span[contains(@class,"price")]//text()').get()
            
            # Se encontrou link, segue para página de detalhes
            if link:
                yield response.follow(link, self.parse_detalhes, meta={
                    'nome': nome,
                    'link': link,
                    'preco_pagina_lista': preco,
                    'playwright': True  # Usar Playwright para páginas de detalhes
                })
        
        # Paginação: seguir para próxima página
        proxima_pagina = response.xpath('//a[contains(@class,"pagination-link") and contains(@class,"next")]/@href | //a[contains(text(),"Próxima")]/@href').get()
        if proxima_pagina:
            yield response.follow(proxima_pagina, self.parse, meta={'playwright': True})

    def parse_detalhes(self, response: scrapy.http.Response):
        """
        Extrai detalhes da página individual do produto
        """
        nome = response.meta.get('nome', '')
        link = response.meta.get('link', '')
        
        # Limpar namespaces
        response.selector.remove_namespaces()
        
        # Extrair nome completo (título da página)
        nome_completo = response.xpath('//h1//text() | //title//text()').get()
        if nome_completo:
            nome_completo = w3lib.html.remove_tags(nome_completo).strip()
        
        # Extrair preço (pode ser que precise de login para ver o preço real)
        preco = response.xpath('//span[contains(@class,"selling-price")]//text() | //span[contains(@class,"vtex-product-price")]//text() | //meta[@property="product:price:amount"]/@content').get()
        
        # Extrair preço antigo/de (se houver promoção)
        preco_de = response.xpath('//span[contains(@class,"list-price")]//text() | //span[contains(@class,"old-price")]//text()').get()
        
        # Extrair marca
        marca = response.xpath('//span[contains(@class,"brand")]//text() | //a[contains(@href,"/marca/")]//text() | //meta[@property="product:brand"]/@content').get()
        
        # Extrair descrição
        descricao = response.xpath('//div[contains(@class,"description")]//text() | //meta[@name="description"]/@content').get()
        
        # Extrair SKU/Referência
        sku = response.xpath('//span[contains(@class,"sku")]//text() | //meta[@property="product:sku"]/@content').get()
        
        # Extrair peso da descrição ou nome (ex: 5kg, 1kg)
        peso_match = re.search(r'(\d+(?:[,.]\d+)?)\s*(kg|g|gr)\b', nome_completo or nome or '', re.IGNORECASE)
        peso = peso_match.group(0) if peso_match else None
        
        # Determinar tipo de arroz pelo nome
        tipo_arroz = None
        nome_lower = (nome_completo or nome or '').lower()
        if 'parboilizado' in nome_lower:
            tipo_arroz = 'Parboilizado'
        elif 'branco' in nome_lower:
            tipo_arroz = 'Branco'
        elif 'integral' in nome_lower:
            tipo_arroz = 'Integral'
        elif '7 grãos' in nome_lower or 'sete grãos' in nome_lower:
            tipo_arroz = '7 Grãos'
        elif 'arbóreo' in nome_lower or 'arborio' in nome_lower:
            tipo_arroz = 'Arbóreo'
        elif 'jasmim' in nome_lower:
            tipo_arroz = 'Jasmim'
        
        # Disponibilidade (se precisa de login para ver preço, indicar isso)
        disponibilidade = response.xpath('//span[contains(@class,"availability")]//text() | //meta[@property="product:availability"]/@content').get()
        precisa_login = preco is None or 'login' in (disponibilidade or '').lower()
        
        produto_info = {
            'nome': nome_completo or nome,
            'marca': marca,
            'tipo_arroz': tipo_arroz,
            'peso': peso,
            'preco': preco,
            'preco_de': preco_de,
            'precisa_login_para_preco': precisa_login,
            'sku': sku,
            'descricao': descricao,
            'url': link,
            'pagina_listagem': response.meta.get('preco_pagina_lista')
        }
        
        yield produto_info