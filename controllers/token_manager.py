import os
import pandas as pd
import json

class TokenManager:

    def __init__(self, context_path, prompt, max_tokens=60_000):
        """
        Inicializa o TokenManager com caminho do arquivo, prompt e limite de tokens.
        
        Args:
            context_path (str): Caminho do arquivo CSV, JSON ou JSONL
            prompt (str): Texto do prompt fixo
            max_total_tokens (int): Limite máximo de tokens (padrão: 60,000)
        """
        self.context_path = context_path
        self.prompt = prompt
        self.max_total_tokens = max_tokens
        
        # Se não houver context_path, apenas calcula tokens do prompt
        if not context_path:
            self.prompt_tokens = self.count_tokens(prompt)
            self.context_data = ""
            self.lines_to_process = 0
            self.remaining_lines = 0
            self.current_tokens = self.prompt_tokens
            self.batch_path = None
            self.batch_tokens = 0
            return
        
        self.file_type = self._detect_file_type(context_path)

        # Criar diretório de saída se não existir
        self.output_dir = './tmp/'
        os.makedirs(self.output_dir, exist_ok=True)

        # Carrega e processa os dados iniciais
        self.load_initial_data()

    def load_initial_data(self):
        """
        Carrega os dados iniciais e calcula o primeiro lote de processamento
        """
        self.context_data = self.read_file_content()
        prompt_tokens = self.count_tokens(self.prompt)

        # Calcula o lote inicial
        self.lines_to_process, self.remaining_lines, self.current_tokens = (
            self.calculate_batch_size(self.context_data, prompt_tokens)
        )

        # Prepara o primeiro lote de dados
        self.prepare_initial_batch(self.context_path, self.lines_to_process)

        # Imprime informações de depuração
        print(f"[DEBUG] Tokens do prompt: {prompt_tokens}")
        print(f"[DEBUG] Tokens do bacth: {self.batch_tokens}")
        print(f"[DEBUG] Tokens da soma do prompt + batch: {prompt_tokens + self.batch_tokens}")

    def _detect_file_type(self, file_path):
        """
        Detecta o tipo de arquivo baseado na extensão.
        
        Args:
            file_path (str): Caminho do arquivo
            
        Returns:
            str: 'csv', 'json' ou 'jsonl'
        """
        _, ext = os.path.splitext(file_path.lower())
        if ext == '.json':
            return 'json'
        elif ext == '.jsonl':
            return 'jsonl'
        elif ext == '.csv':
            return 'csv'
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {ext}. Apenas CSV, JSON e JSONL são aceitos.")

    def read_file_content(self, file_path=None):
        """
        Lê o conteúdo completo do arquivo como string.
        
        Args:
            file_path (str): Caminho do arquivo (opcional)

        Returns:
            str: Conteúdo do arquivo
        """
        # Usa o caminho do contexto como padrão, caso nenhum caminho seja fornecido
        file_path = file_path or self.context_path
        
        # Abrindo o arquivo e lendo seu conteúdo
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def read_csv_content(self, csv_file_path=None):
        """
        Lê o conteúdo completo do CSV como string.
        [MÉTODO MANTIDO PARA COMPATIBILIDADE]
        
        Args:
            csv_file_path (str): Caminho do arquivo CSV (opcional)

        Returns:
            str: Conteúdo do arquivo CSV
        """
        return self.read_file_content(csv_file_path)

    @staticmethod
    def count_tokens(text):
        """
        Conta tokens usando divisão por espaços em branco.

        Returns:
            int: Número de tokens no texto
        """
        return len(text.split()) if text.strip() else 0

    def calculate_batch_size(self, file_content, prompt_tokens, buffer_lines=5):
        """
        Calcula quantas linhas podem ser processadas dentro do limite de tokens.
        
        Args:
            file_content (str): Conteúdo completo do arquivo
            prompt_tokens (int): Tokens do prompt fixo
            buffer_lines (int): Margem de segurança em linhas
            
        Returns:
            tuple: (linhas_processar, linhas_restantes, tokens_totais)
        """
        if self.file_type == 'json':
            return self._calculate_batch_size_json(file_content, prompt_tokens, buffer_lines)
        elif self.file_type == 'jsonl':
            return self._calculate_batch_size_jsonl(file_content, prompt_tokens, buffer_lines)
        else:
            return self._calculate_batch_size_csv(file_content, prompt_tokens, buffer_lines)
    
    def _calculate_batch_size_csv(self, csv_content, prompt_tokens, buffer_lines=5):
        """
        Calcula quantas linhas podem ser processadas dentro do limite de tokens para CSV.
        """
        lines = csv_content.split('\n')
        current_tokens = prompt_tokens * 1.5
        processed_lines = 0

        # Processa as linhas até atingir o limite de tokens
        for line in lines:
            line_tokens = self.count_tokens(line)
            
            # Verifica limite com margem de segurança
            if (self.max_total_tokens) < (current_tokens + line_tokens):
                break
            
            # Adição de tokens e incremento de linhas processadas
            current_tokens += line_tokens
            processed_lines += 1

        # Adição de linhas de buffer e ajuste de linhas processadas
        remaining = len(lines) - processed_lines
    
        return processed_lines, remaining, current_tokens
    
    def _calculate_batch_size_json(self, json_content, prompt_tokens, buffer_lines=5):
        """
        Calcula quantas entradas podem ser processadas dentro do limite de tokens para JSON.
        """
        try:
            data = json.loads(json_content)
            
            # Se for uma lista, processa cada item
            if isinstance(data, list):
                current_tokens = prompt_tokens * 1.5
                processed_items = 0
                
                for item in data:
                    item_tokens = self.count_tokens(json.dumps(item, ensure_ascii=False))
                    
                    # Verifica limite com margem de segurança
                    if (self.max_total_tokens) < (current_tokens + item_tokens):
                        break
                    
                    current_tokens += item_tokens
                    processed_items += 1
                
                remaining = len(data) - processed_items
                return processed_items, remaining, current_tokens
            
            # Se for um objeto único, retorna tudo ou nada
            else:
                total_tokens = prompt_tokens * 1.5 + self.count_tokens(json_content)
                if total_tokens <= self.max_total_tokens:
                    return 1, 0, total_tokens
                else:
                    return 0, 1, prompt_tokens * 1.5
                    
        except json.JSONDecodeError:
            raise ValueError("Arquivo JSON inválido")

    def _calculate_batch_size_jsonl(self, jsonl_content, prompt_tokens, buffer_lines=5):
        """
        Calcula quantas linhas podem ser processadas dentro do limite de tokens para JSONL.
        """
        lines = jsonl_content.strip().split('\n')
        current_tokens = prompt_tokens * 1.5
        processed_lines = 0
        
        for line in lines:
            if not line.strip():  # Pula linhas vazias
                continue
                
            try:
                # Valida se a linha é um JSON válido
                json.loads(line)
                line_tokens = self.count_tokens(line)
                
                # Verifica limite com margem de segurança
                if (self.max_total_tokens) < (current_tokens + line_tokens):
                    break
                
                current_tokens += line_tokens
                processed_lines += 1
                
            except json.JSONDecodeError:
                # Se a linha não for JSON válido, pula
                continue
        
        remaining = len([l for l in lines if l.strip()]) - processed_lines
        return processed_lines, remaining, current_tokens

    def prepare_initial_batch(self, context_path, lines_to_process):
        """
        Prepara o primeiro lote de dados para processamento        

        Args:
            context_path (str): Caminho do arquivo
            lines_to_process (int): Número de linhas/itens a serem processados
        """
        if self.file_type == 'csv':
            dataframe_batch = pd.read_csv(context_path, nrows=lines_to_process)
            self.save_batch_to_csv(dataframe_batch, 'batch_inicial.csv')
        elif self.file_type == 'jsonl':
            batch_data = self._read_jsonl_lines(context_path, lines_to_process)
            self.save_batch_to_jsonl(batch_data, 'batch_inicial.jsonl')
        else:  # JSON
            with open(context_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if isinstance(data, list):
                batch_data = data[:lines_to_process]
            else:
                batch_data = data if lines_to_process > 0 else {}
            
            self.save_batch_to_json(batch_data, 'batch_inicial.json')

    def save_batch_to_csv(self, dataframe, output_path):
        """
        Salva um DataFrame em arquivo CSV.
        
        Args:
            dataframe (pd.DataFrame): Dados a serem salvos
            output_path (str): Caminho do arquivo de saída
            
        Returns:
            str: Caminho do arquivo salvo
        """
        # Caminho completo do arquivo de saída
        output_path = os.path.join(self.output_dir, output_path)

        # Salva o lote em um arquivo CSV
        dataframe.to_csv(output_path, index=False)
        print(f"[DEBUG] Batch armazenado em: {output_path}")

        # Armazena o caminho do arquivo
        self.batch_path = output_path
        self.batch_tokens = self.count_tokens(open(self.batch_path, 'r', encoding='utf-8').read())

        return output_path
    
    def save_batch_to_json(self, data, output_path):
        """
        Salva dados em arquivo JSON.
        
        Args:
            data: Dados a serem salvos
            output_path (str): Caminho do arquivo de saída
            
        Returns:
            str: Caminho do arquivo salvo
        """
        # Caminho completo do arquivo de saída
        output_path = os.path.join(self.output_dir, output_path)

        # Salva o lote em um arquivo JSON
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        print(f"[DEBUG] Batch armazenado em: {output_path}")

        # Armazena o caminho do arquivo
        self.batch_path = output_path
        self.batch_tokens = self.count_tokens(open(self.batch_path, 'r', encoding='utf-8').read())

        return output_path
    
    def save_batch_to_jsonl(self, data, output_path):
        """
        Salva dados em arquivo JSONL.
        
        Args:
            data (list): Lista de objetos a serem salvos
            output_path (str): Caminho do arquivo de saída
            
        Returns:
            str: Caminho do arquivo salvo
        """
        # Caminho completo do arquivo de saída
        output_path = os.path.join(self.output_dir, output_path)

        # Salva o lote em um arquivo JSONL
        with open(output_path, 'w', encoding='utf-8') as file:
            for item in data:
                json.dump(item, file, ensure_ascii=False)
                file.write('\n')
        
        print(f"[DEBUG] Batch armazenado em: {output_path}")

        # Armazena o caminho do arquivo
        self.batch_path = output_path
        self.batch_tokens = self.count_tokens(open(self.batch_path, 'r', encoding='utf-8').read())

        return output_path
    
    def _read_jsonl_lines(self, file_path, num_lines):
        """
        Lê um número específico de linhas de um arquivo JSONL.
        
        Args:
            file_path (str): Caminho do arquivo JSONL
            num_lines (int): Número de linhas a serem lidas
            
        Returns:
            list: Lista de objetos JSON
        """
        data = []
        lines_read = 0
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if lines_read >= num_lines:
                    break
                    
                line = line.strip()
                if not line:  # Pula linhas vazias
                    continue
                    
                try:
                    json_obj = json.loads(line)
                    data.append(json_obj)
                    lines_read += 1
                except json.JSONDecodeError:
                    # Se a linha não for JSON válido, pula
                    continue
        
        return data
    
    def get_batch_path(self):
        """
        Retorna o caminho do arquivo do lote.
        
        Returns:
            str: Caminho do arquivo do lote
        """
        return self.batch_path
    
    def get_file_type(self):
        """
        Retorna o tipo do arquivo sendo processado.
        
        Returns:
            str: 'csv' ou 'json'
        """
        return self.file_type
    
    def is_json_file(self):
        """
        Verifica se o arquivo é do tipo JSON.
        
        Returns:
            bool: True se for JSON, False caso contrário
        """
        return self.file_type == 'json'
    
    def is_csv_file(self):
        """
        Verifica se o arquivo é do tipo CSV.
        
        Returns:
            bool: True se for CSV, False caso contrário
        """
        return self.file_type == 'csv'
    
    def is_jsonl_file(self):
        """
        Verifica se o arquivo é do tipo JSONL.
        
        Returns:
            bool: True se for JSONL, False caso contrário
        """
        return self.file_type == 'jsonl'
    
    def get_number_of_rows(self, file_path=None, string_content=None):
        """
        Retorna o número de linhas em um arquivo CSV, itens em um JSON ou linhas em um JSONL.

        Args:
            file_path (str): Caminho do arquivo
            string_content (str): Conteúdo do arquivo como string
        
        Returns:
            int: Número de linhas/itens no arquivo
        """

        # Se o caminho do arquivo não for fornecido, usa o caminho do lote
        if file_path is not None:
            # Lê o conteúdo do arquivo
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Detecta o tipo de arquivo
            _, ext = os.path.splitext(file_path.lower())
            if ext == '.json':
                file_type = 'json'
            elif ext == '.jsonl':
                file_type = 'jsonl'
            else:
                file_type = 'csv'
        else:
            content = string_content
            # Tenta detectar se é JSON ou JSONL pelo conteúdo
            file_type = 'csv'  # padrão
            if string_content and string_content.strip().startswith('{') or string_content.strip().startswith('['):
                try:
                    json.loads(string_content)
                    file_type = 'json'
                except:
                    # Se não for JSON válido, pode ser JSONL
                    lines = string_content.strip().split('\n')
                    if len(lines) > 1:
                        try:
                            json.loads(lines[0])
                            file_type = 'jsonl'
                        except:
                            pass

        if file_type == 'json':
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    return len(data)
                else:
                    return 1 if data else 0
            except json.JSONDecodeError:
                return 0
        elif file_type == 'jsonl':
            # Conta o número de linhas válidas de JSON no JSONL
            lines = content.strip().split('\n')
            valid_lines = 0
            for line in lines:
                if line.strip():
                    try:
                        json.loads(line)
                        valid_lines += 1
                    except json.JSONDecodeError:
                        continue
            return valid_lines
        else:
            # Conta o número de linhas no conteúdo do CSV
            return len(content.split('\n')) if content.strip() else 0