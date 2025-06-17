import os
import json
import pandas as pd

class PromptTemplate:
    """
    Classe para gerar um template de prompt para análise de dados de saúde mental.
    """

    def __init__(self, context):
        """
        Inicializa a classe com os dados do paciente e URLs de imagens.
        
        Args:
            context (str): Contexto para o prompt, incluindo dados do paciente e URLs de imagens.
        """

        # Verifica se o caminho do arquivo existe
        self.context = context

        # Cria o template do prompt com o formato esperado
        self.create_prompt_template(self.context)

    def create_prompt_template(self, context):
        """
        Gera o prompt, incluindo uma nova seção e instruções para as imagens.

        Args:
            context (str): Contexto para o prompt, incluindo dados do paciente e URLs de imagens.

        Returns:
            str: O prompt formatado.
        """

        self.prompt = f"""
        <context>
            You are a specialized board game analyst with extensive experience in game mechanics evaluation and strategy analysis. 
            Your task is to analyze player game session data from multiple sessions and produce a comprehensive gaming performance summary.
            This summary should also incorporate any provided game images in a visually organized manner.
        </context>
        
        <instructions>
            INSTRUCTIONS:
            1. Analyze the player's game session data from different sessions thoroughly.
            2. Produce ONE comprehensive gaming performance summary for the player.
            3. The output format MUST be HTML.
            4. The summary must be enclosed in <html></html> tags.
            5. Include a professional gaming assessment based on session patterns and gameplay content.
            6. Focus on gaming performance, strategies, and behavioral patterns across different sessions.
            7. Use a proper HTML structure with headers and lists. The analysis in each section MUST be in bullet points using styled <ul> and <li> tags.
            8. Be thorough but concise in your analysis.
            9. Include the following sections in this exact order:
               - Header: Player Name, GUID, Date of Registration, Contact Information
               - Gaming Summary
               - Strategies and Performance Issues: Key reported strategies and gaming history
               - Gaming Factors: Session frequency, game preferences, competitive level, and social gaming habits
               - Gaming Keywords: Extracted from the sessions, including keywords like strategy games, cooperative play, competitive gaming
               - Performance Notes: Recommendations or flagged areas for improvement
               - Attachments: Any uploaded documents (e.g., game photos, scorecards, strategy notes)
            10. If images are provided in the <player_images> section (which contains a list of URLs), you MUST create a "Attachments" section immediately after the "Performance Notes" section.
            11. In the "Attachments" section, display each image using an `<img>` tag with the `src` attribute set to the provided URL. Organize the images in a clean grid or gallery layout for a professional appearance.
            12. Maintain professional gaming analysis language and standards.
            13. Identify patterns and changes in gaming performance across different session days.
            14. The title MUST be exactly: <head><title>Player Gaming Performance Summary</title></head>
            15. Add a final section at the end of the HTML document titled "Session References" that lists only the file keys/paths where the session data is stored using structured format (table format recommended with only one column for File Key)
        </instructions>

        <context>
            {context}
        </context>
        """
        
        return self.prompt
    
    def get_prompt_text(self):
        """
        Retorna o texto do prompt formatado.
        """
        return self.prompt