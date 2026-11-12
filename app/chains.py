import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="openai/gpt-oss-120b")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text above is from the careers page of a company website.
            Extract every job posting found in the text and return them as a JSON array,
            where each object contains the following keys:
            - `role`: the job title (string)
            - `experience`: the required experience level or years (string, use "" if not mentioned)
            - `skills`: a list of technical skills/technologies required (array of strings)
            - `description`: a concise 1-2 sentence summary of the role (string)

            Rules:
            - If the text contains no job postings, return an empty array: []
            - Do not invent or infer information that isn't present in the text.
            - Return ONLY the JSON array, with no markdown code fences, no explanation, and no preamble.

            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Idrissa, an engineering student at Polytech Lyon, currently exploring opportunities in AI/software development and machine learning.

            Your task is to write a cold email to the company whose job posting is described above, expressing genuine interest in the role and highlighting your relevant skills and academic background.
            The email should:
            1. Open with a brief, relevant hook connected to the specific role/need described in the job posting (avoid generic openers like "I hope this finds you well").
            2. Briefly explain why your profile (engineering student at Polytech Lyon, with a focus on AI/software) is a good fit for this specific opportunity — be concrete, not generic.
            3. Include the 2-3 most relevant links from the following portfolio to demonstrate relevant projects or experience: {link_list}
            4. End with a clear, low-friction call to action (e.g. proposing a short call or interview), and sign off as Idrissa.

            Constraints:
            - Keep the email under 150 words.
            - Write in a professional but natural, non-salesy tone.
            - Do not invent details about the company or job posting not present in the description.
            - Do not use generic filler phrases ("I hope this finds you well", "I am excited to", "cutting-edge").
            - Do not provide a preamble or any text outside the email itself.

            Structure the email as follows, with a blank line between each part:
            - Greeting line
            - Opening hook (1-2 sentences)
            - Value proposition + relevant portfolio links (2-3 sentences)
            - Call to action + sign-off

            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

