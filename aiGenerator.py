from litellm import completion


class LLMToSQL:
    def __init__(self):
        self.database = "MyDatabase"
        self.tablesData = "users (id, name, surname, email, depart_id(foreign key)), departments (depart_id(primary key), depart_name)"

    def _replace_variables(self, prompt, input_instruction):
        prompt = prompt.replace("${database}", self.database)
        prompt = prompt.replace("${tablesData}", self.tablesData)
        prompt = prompt.replace("${input}", input_instruction)

        return prompt

    def complete(self, input_instruction):
        prompt_template = (
            "In the database named: ${database}, you have the following tables and their columns as follows: ${tablesData}. "
            "Write a query to perform the following task: ** ${input} ** "
            "Write only query, don't give any explanations or other context about it. "
            "Remember that the query should be valid SQL syntax and joins are preferred if needed rather than subqueries. "
            "Also keep note that the query should be optimized and should not be too complex. "
            "Keep it as simple as possible"
            "If the request is simple, there is no need to use JOIN")

        prompt_content = self._replace_variables(prompt_template, input_instruction)

        message = {
            "content": prompt_content,
            "role": "user"
        }

        response = completion(
            model="ollama/deepseek-coder:6.7b",
            messages=[message],
            api_base="http://localhost:11434",
            max_tokens=50,
        )

        return response


llm_to_sql = LLMToSQL()
inputInstruction = "Show me all users that are working in \"HR\" department."
response = llm_to_sql.complete(inputInstruction)
exactResponse = response.choices[0].message.content
print("Input: ", inputInstruction)
print(exactResponse)
