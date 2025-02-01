# ZecureFi

## ABOUT
**Zecure-Fi** is a **zero knowledge based protocol** with an inbuilt **AI-agent** which helps problem of borrowers taking loan in **undercollaterized** manner from lenders by providing the lender their **financial history** at various **protocols and decentralized exchanges** in zero knowledge manner and gets **verified** for their financial status and if the borrower **crosses the loan threshold financial score** set by the Lender while creating a loan they can create borrow requests which in turn will be accepted or rejected by the Lender based on other borrow requests other borrowers made.

**AI agent** is built using Coinbase Agent Kit by **adding tools for various decentralized protocols and exchanges** and for every wallet address a new agent is made which helps in **trading** and making **estimate analysis of tokens and market** to the connected user in app.

## ARCHITECTURE

## ![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](./public/project_architecture.png)

## PROJECT SETUP

- Clone the repository using :-

```
git clone https://github.com/kaurjasleen240305/No-name
                   or
git clone git@github.com:kaurjasleen240305/No-name.git
```

- To start the frontend run and check ```http://localhost:3000```:-
```
cd frontend
npm install
npm run dev
```

-To start the flask server for AI agent run and check ```http://localhost:5000```:-
```
pip install -r requirements.txt
python chatbot-flask.py
```