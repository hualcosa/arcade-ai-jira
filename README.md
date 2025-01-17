# jira

toolkit designed to perform basic operations on JIRA Issues

## How to setup the toolkit:
. [Install the Arcade Engine Locally](https://docs.arcade-ai.com/home/install/local)
2. Install extra dependencies needed for evals:
   ```bash
   pip install 'arcade-ai[fastapi,evals]'
   ```
3. Log into Arcade AI:
   ```bash
   arcade login
   ```
4. Add the Jira cloud credentials to the ~/.arcade/arcade.env file:
   ```bash
   JIRA_API_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXX
   JIRA_EMAIL=example@example.com
   JIRA_BASE_URL=https://example.atlassian.net
   ```

   To obtain these credentials:
   1. **JIRA_API_TOKEN**: 
      - Log in to https://id.atlassian.com/manage/api-tokens
      - Click "Create API token"
      - Give your token a label and click "Create"
      - Copy the generated token (you won't be able to see it again)
   
   2. **JIRA_EMAIL**:
      - Use the email address associated with your Atlassian account
   
   3. **JIRA_BASE_URL**:
      - This is your Jira instance URL (e.g., https://your-domain.atlassian.net)
      - For cloud instances, it will be in the format: https://[your-domain].atlassian.net

## How to install the toolkit:
1. Run `make install` from the root of the repository

## How to run tests:
1. Run `make test` from the root of the repository

## How to run evals:
1. [Install the Arcade Engine Locally](https://docs.arcade-ai.com/home/install/local)
2. Install extra dependencies needed for evals:
   ```bash
   pip install 'arcade-ai[fastapi,evals]'
   ```
3. Log into Arcade AI:
   ```bash
   arcade login
   ```
4. Start the Arcade Engine and Actor:
   ```bash
   arcade dev
   ```
5. In a separate terminal, navigate to the `evals` directory:
   ```bash
   cd evals
   ```
5. Run the evals:
   ```bash
   arcade evals --host localhost --details
   ```