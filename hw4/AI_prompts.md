# HW4 AI Prompts Log

This file records the prompts used for each homework problem. Each problem entry includes its number and title, the first prompt verbatim, any follow-up prompt verbatim, and corrections needed to the first prompt.

## Problem 1: Take the zip file data.zip that I just downloaded to my Downloads folder, and then unzip into this folder. It should yield 3 files - data/campus\_customs.db, and data/products/

### 1. First prompt (verbatim)

Take the zip file data.zip that I just downloaded to my Downloads folder, and then unzip into this folder. It should yield 3 files - data/campus\_customs.db, and data/products/

### 2. Follow-up prompts (verbatim)

Oh it's data (2)

Whaat do you mean by problem 1 title?

The file is actually named data (2).zip - pull that in. For the problem 1 title, just put the first prompt I sent you that initiated us working on this part of the HW.

### 3. Corrections needed in the first prompt

The correct archive filename was `data (2).zip`, not `data.zip`.

## Problem 2: Open up the data/campus\_customs.db for me. Then start the file output/harness.md  - I will dictate to you what to add to that .md file..

### 1. First prompt (verbatim)

Open up the data/campus\_customs.db for me. Then start the file output/harness.md  - I will dictate to you what to add to that .md file..

### 2. Follow-up prompts (verbatim)

Can you open up that file here in VScode?

Wait no open up the .db file here

Wait are we in HW2 or HW4?

Can you send me here a bit of a summary under each of the .db data cateogries (catalogue, inventory, chat\_messages, users) a quick summary of what is included in each?

Okay great. I need you to add to the output/harness.md a section that outlines 1) each table in the .db file, 2) its fields, and then I'm going to add one short line on why each field matters. Prompt me to add a line for each field on why they matter to the later steps.

Great. Can you open up the output/harness.md for me so I can add descriptors directly into the .md file?

Can you give me 2-3 lines of what the 'description' category contains in the catalogue table?

Oh great. That is a really helpful descriptor. Can you do that for all of the fields in each table  in harness.md? I started it for 'catalogue' but I'd like you to continue it

Take that out of AI\_prompts.md, it should just be in output/harness.md. Add it in the *Add one short line* section

Wait can  you re-open harness.md so I can see the changes?

Can you re-open that for me I can't see it?

### 3. Corrections needed in the first prompt

The requested file to open in VS Code was `data/campus_customs.db`, not `output/harness.md`.

## Problem 3: Great. We're now on Problem 3. We're now going to create the Campus Customs website, that will eventually have a helpful chatbot. For this problem, we're going to scaffold a React + VIte + TypeScript front end for Campus Customs site. Put a nav bar at the top that links to these main pages: Home; Products; About Us; Log In; Create Account. On the 'Home' page, the copy on the intro should read 'Repping the Bulldog Blue: Officially Licensed Merchandise'. The 'About Us' section should read - 'Did you or a loved on go to Yale and you don't ever want to shut up about it? You don't have to! Wear your Bulldog Blue pride through our selection of official merchandise, or find that perfect gift for your favorite Yale student, alumnus, relative, or friend.'

### 1. First prompt (verbatim)

Great. We're now on Problem 3. We're now going to create the Campus Customs website, that will eventually have a helpful chatbot. For this problem, we're going to scaffold a React + VIte + TypeScript front end for Campus Customs site. Put a nav bar at the top that links to these main pages: Home; Products; About Us; Log In; Create Account. On the 'Home' page, the copy on the intro should read 'Repping the Bulldog Blue: Officially Licensed Merchandise'. The 'About Us' section should read - 'Did you or a loved on go to Yale and you don't ever want to shut up about it? You don't have to! Wear your Bulldog Blue pride through our selection of official merchandise, or find that perfect gift for your favorite Yale student, alumnus, relative, or friend.'

### 2. Follow-up prompts (verbatim)

Nice. Here's the second prompt for Problem 3. on the 'Products' page in the site, please show product images from the catalogue via the image paths in the database, including basic product info (name, price, short descriptor). Each product should be hyperlinked to a single-item page that includes a large image on one side, full product text on th eother (incl. description, price, sizes / stock when you have them) and clicking a card on 'Products' should take the shopper there to that specific page. On the bottom right, add a chat interface - we'll set up the backend in the later problem. Start a simple FastAPI app in backend/main.py to serve products and images to read the database.

Okay run it, and then send me a viewable link

### 3. Corrections needed in the first prompt

_To be determined._

## Problem 4: Great. Let's move onto problem 4. We're going to create a normal create-account/login flow. Create account should include prompts to include your first name, last name, email, password, and a confirm password line. These shoulld be text entry fields. For email, it should be able to validate that the entry is formatted like an email address. For password and confirm password, they should contain the exact same text, case sensitive like a password, otherwise the user shouldn't be abe to proceed. Then there should be a separate log in page that prompts for email and password. New accounts should automatically get uploaded into the 'users' table. Make sure the passwords are stored securely in the table so they can't be accessed. I'd like to test with credentials that are already in the 'user' file that should work - the email is test\@campuscustoms.yale.edu and Password is password. Update output/harness.md with how the auth works, including what is stored, and how passwords are protected.

### 1. First prompt (verbatim)

Great. Let's move onto problem 4. We're going to create a normal create-account/login flow. Create account should include prompts to include your first name, last name, email, password, and a confirm password line. These shoulld be text entry fields. For email, it should be able to validate that the entry is formatted like an email address. For password and confirm password, they should contain the exact same text, case sensitive like a password, otherwise the user shouldn't be abe to proceed. Then there should be a separate log in page that prompts for email and password. New accounts should automatically get uploaded into the 'users' table. Make sure the passwords are stored securely in the table so they can't be accessed. I'd like to test with credentials that are already in the 'user' file that should work - the email is test\@campuscustoms.yale.edu and Password is password. Update output/harness.md with how the auth works, including what is stored, and how passwords are protected.

### 2. Follow-up prompts (verbatim)

Okay one quick update - the Email address input on the 'Welcome back' page should match to an active user in the 'users' table, and then the password should correspond to that email in the table.

The test email isn't working tho

OKay it's still not working, but perhaps I should specify that when you log in, you should be able to see that you are shopping as that account. Somewhere on the site it should address that a specific shopper is shopping like 'Hello 'First Name''

I keep getting the error 'Please match the requested format' in the email Log In page - why is that? Can you correct that? There shouldn't be that error on the Log In, only on the 'Create Account' workflow

Great it works. That's the end of problem 4. The next prompt I give will be problem 5

### 3. Corrections needed in the first prompt

_To be determined._

## Problem 5: We're now going to build the shop chatbot as a PydanticAI agent behind FastAPI, plugged into the front-end chat widget. Put the API app in backend/main.py - this is the file we'll run with Uvicorn. Keep the agent as the fese four files next to it: backend/prompts/prompt.md - system prompt (we'll grow this file later), backend/agent.py - agent entry / wiring; backend/tools.py - toold the agent can call and then backend/models.py - the Pydantic / PydanticAI structured type. In main.py expose a chat route so a message from the website returns a reply from the agent. The chat interface should be connected to a FastAPI /chat endpointswhich will take the user's message to the agent and return the response in the frontend. Put some voice and safety basics into prompts/prompts.md and start or update types in models.py for chat replies / product cards sa needed. In output/harness.md, add a note on how the front end talks to FastAPI and how the agent is loaded with the prompt file + model. Make sure the backend can run from the backend/ folder like this uvicorn main:app --reload --port 8000 . And go ahead and run everything!

### 1. First prompt (verbatim)

We're now going to build the shop chatbot as a PydanticAI agent behind FastAPI, plugged into the front-end chat widget. Put the API app in backend/main.py - this is the file we'll run with Uvicorn. Keep the agent as the fese four files next to it: backend/prompts/prompt.md - system prompt (we'll grow this file later), backend/agent.py - agent entry / wiring; backend/tools.py - toold the agent can call and then backend/models.py - the Pydantic / PydanticAI structured type. In main.py expose a chat route so a message from the website returns a reply from the agent. The chat interface should be connected to a FastAPI /chat endpointswhich will take the user's message to the agent and return the response in the frontend. Put some voice and safety basics into prompts/prompts.md and start or update types in models.py for chat replies / product cards sa needed. In output/harness.md, add a note on how the front end talks to FastAPI and how the agent is loaded with the prompt file + model. Make sure the backend can run from the backend/ folder like this uvicorn main:app --reload --port 8000 . And go ahead and run everything!

### 2. Follow-up prompts (verbatim)

_No follow-up; Problem 5 ended before the catalogue-tools request._

### 3. Corrections needed in the first prompt

_To be determined._

## Problem 6: Great. Now we're going to give the agent tools to look up info from the campus\_customs.db file. I'd like the agent to look up product description, price, how many are in stock (by size when the customer asks). The agent must use the exact text from the database - do NOT invent prices or quantities, and if a size is out of stock make that clear. Add to prompts/prompts.md so the agent knows to call these tools for any inquiries related to price and stock. Add or update return types in models.py. In output/harness.md, list each of the tools and explain which model fields you chose for lookup results and then a justification of why we chose those fields.

### 1. First prompt (verbatim)

Great. Now we're going to give the agent tools to look up info from the campus\_customs.db file. I'd like the agent to look up product description, price, how many are in stock (by size when the customer asks). The agent must use the exact text from the database - do NOT invent prices or quantities, and if a size is out of stock make that clear. Add to prompts/prompts.md so the agent knows to call these tools for any inquiries related to price and stock. Add or update return types in models.py. In output/harness.md, list each of the tools and explain which model fields you chose for lookup results and then a justification of why we chose those fields.

### 2. Follow-up prompts (verbatim)

Oh sorry this is all under problem 6! the last prompt I sent is prob 6, the ones before it were the end of problem 5.

Great. did you complete the Problem 6 prompt already?

### 3. Corrections needed in the first prompt

_To be determined._

## Problem 7: Great - we are now on problem 7. We're going to create an API contract where the agent is going to return a structured product match and the front end will render onto the website dynamically showing those matching items as product cards (image, name, price, short info)- this should be for when a customer asks questions like "What hoodies do you have?" Once implemented, double check the website to ensnure that the Problem 3 feature of each product having its own singgle-item page you can access by clicking on the product card - still works. Lastly, update prompts/prompt.md and output/harness.md with how search results reach the page.

### 1. First prompt (verbatim)

Great - we are now on problem 7. We're going to create an API contract where the agent is going to return a structured product match and the front end will render onto the website dynamically showing those matching items as product cards (image, name, price, short info)- this should be for when a customer asks questions like "What hoodies do you have?" Once implemented, double check the website to ensnure that the Problem 3 feature of each product having its own singgle-item page you can access by clicking on the product card - still works. Lastly, update prompts/prompt.md and output/harness.md with how search results reach the page.

### 2. Follow-up prompts (verbatim)

N/A - no other prompt needed

### 3. Corrections needed in the first prompt

N/A - no other prompt needed

## Problem 8: Great. End of problem 7, we're now on problem 8. For problem 8, we're going to make sure that the site can remember a customer who is logged in. Guests can still chat, but history should be logged only for logged-in users. When a shopper is logged in, save the chat history in the database in an appropriate table and make sure it's reloaded when they return. Teh agent should be able to know who is chatting with their name and email, and then put that in the agent deps (or an equivaleent clear pattern) with tools the agent can call. Also, insert a bit of code into the agent so that they know if someone is on a product page what they're asking about - i.e., the page context - so that if they ask for example if they have this in pink, or another question like that, the agent knows what the user is talking about.

### 1. First prompt (verbatim)

Great. End of problem 7, we're now on problem 8. For problem 8, we're going to make sure that the site can remember a customer who is logged in. Guests can still chat, but history should be logged only for logged-in users. When a shopper is logged in, save the chat history in the database in an appropriate table and make sure it's reloaded when they return. Teh agent should be able to know who is chatting with their name and email, and then put that in the agent deps (or an equivaleent clear pattern) with tools the agent can call. Also, insert a bit of code into the agent so that they know if someone is on a product page what they're asking about - i.e., the page context - so that if they ask for example if they have this in pink, or another question like that, the agent knows what the user is talking about.

### 2. Follow-up prompts (verbatim)

To finalize problem 8, document in output/harness.md how the user chat history is stored, what customer fields the agent will see and how page context is passed along

### 3. Corrections needed in the first prompt

The first prompt did not explicitly request the final harness documentation details, so this follow-up clarified that the storage model, agent-visible customer fields, and page-context handoff must be documented.

## Problem 9: Frontend and Backend Usability Improvements

### 1. First prompt (verbatim)

Great. End of P8, now on problem 9. I'm going to give you 2 frontend improvements to run, and 2 backend improvements to run. Before we do that, please swrite output/usability.md and put in that .md 1) each of the improvements and 2) why it helps a campus customs shopper or business - i wil give you a version of this but please clean up for comprehension and grammar / spelling.

### 2. Follow-up prompts (verbatim)

For frontend improvements 1) add a feature that allows logged in people to 'woof' at an item, or save it. Make sure that you log in the history that this item was saved, and have this feature be available on both the products page but also on the individual product page. It should be a little pawprint you press that allows you to denote that you want to save it, and then a logged in user should be able to see a page that says 'Your Woofs' of products you want to save - this should help users efficiently revisit the site and the purchases they'd like. 2) Put the 'Log In' and 'Create Account' buttons next to the 'shop the collection' button on the top right. This is a more intuitive placement rather than where it is today as a similar hierarchy as the actual shop pages. For backend improvements 1) Improve the agent's short-term conversational context so it can correctly resolve references like “this,” “that one,” and “the other one” based on the current conversation and product page context. Preserve the existing database-backed behavior and make sure the agent still uses exact product data rather than guessing when the reference is ambiguous. and then 2) Add robust backend error handling for database failures, invalid product IDs, malformed requests, and agent/tool failures. The agent should return a clear, user-friendly response when something goes wrong and should never invent product information to compensate for a failed database lookup.

The 'woofs' funcitonality isn't working on my end - can you double check to make sure it works on the 'products' view and then on the individual 'product' level? Also add some instruction next to he button on the individual page that says 'Woof at it for next time' or something clearer

Please improve and verify the Woof functionality from the user experience side. I want a logged-in user to be able to click the Woof button on both the Products catalogue cards and the individual Product detail page, with the button clearly showing whether that product is currently saved. Clicking it should save the product to the logged-in user's "Your Woofs" section, and clicking it again should remove it. Guests should not be able to save Woofs.
On the individual product page, place a short instruction directly next to or underneath the Woof button that clearly explains its purpose, such as "Woof it to save for next time." Make the saved/unsaved state visually obvious and consistent between the catalogue and detail page. Please test the actual frontend interactions in both locations, not just the API, and make sure "Your Woofs" displays the saved products correctly after navigating away and returning.
Lastly, make sure on the frontend it's reflected that you can see the 'woof' by it turning a different color.

### 3. Corrections needed in the first prompt

The first prompt established the four improvement categories but did not include their descriptions. This follow-up supplied the requirements and rationales to document and implement.

## Problem 10: Campus Customs Visual Redesign and Product Categories

### 1. First prompt (verbatim)

Great. We're done with this problem, on to problem 10. We're going to make lots of cosmetic updates to make this look better. I'd like you to redo the design to remove the yellow, and lean more into the blue and gray, and then let's also make a layout that has cartoon elements of yale campus, like iconic buildings, trees and foliage - goal of this is to make each user feel like they're visiting campus when they visit the site, increasing the 'fun' element. Under the 'find your new favorite' section on the homepage, put actual photos of the items not just cards to make the user experience more clear. To aadd to the fun element as well, change the cursor to be a pawprint (different than the woof button - just a single one). To improve retention, change for 'Guests' the 'create account' button on the top right to be 'Join the Pack'. Under the 'Product' header, make it open into a sub menu that lists and links to product categories, which allows folks to group products by their type (this should be somewhere in the database).

### 2. Follow-up prompts (verbatim)

Can you take a pass at grouping all of the products into categories based on how similar they are, and then list those categories under the 'Products' tab - think like 'short sleeves', 'long-sleeves', 'sweatshirts' stuff like that

### 3. Corrections needed in the first prompt

The original category menu used each database garment type as a separate category. The follow-up clarified that similar garment types should be grouped into shopper-friendly categories.

## Problem 11: Live Site Checks and Screenshot Documentation

### 1. First prompt (verbatim)

Great. That was end of problem 10. Now on to problem 11! We're going to test the live site and document this check in output/app\_check.html. I'm going to perform 3 checks, each with a screenshot of the check to show that it works. Make sure this check HTML is easy for a grader to view with headings for each check, the screenshot, 1-2 sentences on what the scereenshot proves (which I will provide for you) and then put the screenshot image files in output/app\_check\_images/ and link them from app\_check.html with relative paths (example: app\_check\_images/inventory.png)

### 2. Follow-up prompts (verbatim)

This prompt is for Problem 11. I have already placed the Check 1 screenshot at:

`output/app_check_images/check 1.png`

Please update only `output/app_check.html` for Check 1.

Replace the Check 1 placeholder with:

- A clear heading describing the inventory accuracy check
- The embedded image using the relative path `app_check_images/check-1.png`
- A 1–2 sentence explanation stating that the screenshot shows the inventory reported by the Campus Customs chat for both sizes matching the inventory shown on the individual product page

Leave Checks 2 and 3 unchanged.

Do not modify application code, backend code, frontend code, or any other files.

I have already placed the Check 2 screenshot at:

`output/app_check_images/check-2.png`

Please update only `output/app_check.html` for Check 2.

Replace the Check 2 placeholder with:

- A clear heading describing the dynamic product card check
- The embedded image using the relative path `app_check_images/check-2.png`
- A 1–2 sentence explanation stating that the screenshot shows the Campus Customs chat agent returning dynamic product cards when the user searches for a merchandise category, with the cards displaying the relevant product information.

Leave Checks 1 and 3 unchanged.

Do not modify application code, backend code, frontend code, or any other files.

I have already placed the Check 3 screenshot at:

`output/app_check_images/check-3.png`

Please update only `output/app_check.html` for Check 3.

Replace the Check 3 placeholder with:

- A clear heading describing the product category dropdown check
- The embedded image using the relative path `app_check_images/check-3.png`
- A 1–2 sentence explanation stating that the screenshot demonstrates the Products dropdown allowing customers to select a specific merchandise category and navigate to a dedicated page displaying products from that category.

Leave Checks 1 and 2 unchanged.

Do not modify application code, backend code, frontend code, or any other files.

### 3. Corrections needed in the first prompt

N/A - no correction needed.

## Problem 12: Agent Audit Trail and Safety Rules

### 1. First prompt (verbatim)

Nice. we're on problem 12 now where we're going to keep an append-only output/audit_trail.json of agent-loop activiity, including time, tool name, short args / results, stop reason so we can look at the file and see what our agent actually does. Notably, don't erase the existing entries every time you run the agent - new runs should append the file. Then, we're also going to add some safety rules to prompts/prompt.md . These safety rules include: Only answer questions related to Campus Customs/products.&#x20;

1. &#x20;Don't invent product information, prices, inventory, etc.&#x20;
2. &#x20;Use the database/tools for product information rather than making things up.&#x20;
3. &#x20;Don't expose private user information.&#x20;
4. &#x20;Don't perform actions the user hasn't requested.

### 2. Follow-up prompts (verbatim)

The Problem 12 audit trail is not recording actual agent activity. `output/audit_trail.json` remains `[]` even after I use the Campus Customs chat and ask a product question.

Please debug and fix the existing audit logging implementation.

Requirements:

- Trace the actual frontend `/chat` request through the backend agent execution and catalogue tool calls.
- Identify why those real runs are not producing entries in `output/audit_trail.json`.
- Make the smallest necessary fix so actual agent runs and relevant catalogue tool calls are recorded.
- Preserve the append-only behavior. Do not clear or overwrite existing audit entries when a new run occurs.
- Each audit entry should include the information required by Problem 12, including a timestamp, the relevant tool/action, a concise record of arguments or result, and the reason the agent stopped when applicable.
- Do not create fake or hard-coded audit entries just to make the file non-empty.
- Test the fix using an actual `/chat` request, not only the audit helper or a standalone smoke test.
- Run a second chat request and verify that the second run appends to the existing entries rather than replacing them.
- Keep the existing four safety rules unchanged.
- Do not modify the frontend unless the frontend is actually preventing the backend `/chat` request from reaching the audit code.

After testing, report:

1. What was preventing the entries from being written.
2. What you changed.
3. How many audit entries existed after the first real chat.
4. How many existed after the second real chat.
5. Confirm that the original entries were preserved.

Nice. Final Problem 12 prompt - finish output/harness.md so it has a clear outlien of how the system works. Include the model fields in models.py and why we chose them, all of the tools and abilities, safety rules I prescribed, and then specs like loop limits, result caps, models, how to run front end and backend, all that jazz).

### 3. Corrections needed in the first prompt

_To be determined._
## Problem 13: GitHub Submission Preparation

### 1. First prompt (verbatim)

Great! We're now on problem 13, where we're going to push to git! this is the final submission step for my HW

Before committing or pushing anything, audit the current HW4 repository against the Problem 13 requirements.

Check:

- The project is structured so the GitHub repository will contain an `hw4/` folder with the expected files and folders.
- `AI_prompts.md` exists.
- `requirements.txt` exists.
- `.env.example` exists and contains placeholders only.
- `.gitignore` exists and properly excludes `.env`, `data/campus_customs.db`, product images, and other local-only/secrets files.
- `README.md` exists and explains how to run the frontend and backend after placing the local data pack.
- `frontend/` exists.
- `backend/main.py`, `backend/agent.py`, `backend/models.py`, `backend/tools.py`, and `backend/prompts/prompt.md` exist.
- `output/harness.md`, `output/design.md`, `output/usability.md`, `output/app_check.html`, `output/app_check_images/`, and `output/audit_trail.json` exist.
- Confirm that the three app-check screenshots referenced by `output/app_check.html` are present with the correct filenames.
- Check for any secrets, real `.env` files, `campus_customs.db`, product images, or other files that should NOT be pushed.

Do not commit or push anything yet.

Report:

1. What is ready.
2. What is missing.
3. What should be added to `.gitignore`.
4. Any files that would be dangerous or incorrect to commit.
5. Any structural issue that could prevent the grader from opening the repository correctly.

Do not modify application code.

### 2. Follow-up prompts (verbatim)

I completed the Problem 13 repository audit. Please prepare the HW4 project for the required GitHub submission structure, but do NOT commit or push anything yet.

The official required structure is:

hw4/\\
├── AI_prompts.md\\
├── requirements.txt\\
├── .env.example\\
├── .gitignore\\
├── README.md\\
├── frontend/\\
├── backend/\\
└── output/

Please make the following changes:

1. Create a submission folder named `hw4` containing the current HW4 project.
2. Put the existing Vite React TypeScript frontend inside `hw4/frontend/`. Preserve the existing working frontend exactly as much as possible. Move/copy the existing root-level frontend files (`src`, `package.json`, Vite config, TypeScript config, public assets, etc.) into `frontend/` as needed. Do not rewrite the application.
3. Keep the existing `backend/` and `output/` directories under `hw4/`.
4. Create `hw4/requirements.txt` based on the dependencies actually required by the backend. Do not invent unrelated dependencies. It is fine to retain `backend/requirements.txt` if useful, but the required root-level file must exist.
5. Create `hw4/.env.example` containing placeholders only. Do not copy or expose any real API keys, passwords, or secrets.
6. Create `hw4/README.md` explaining:
   - what Campus Customs is
   - that the local data pack must be placed in `data/`
   - how to start the backend using:
     `cd backend`
     `uvicorn main:app --reload --port 8000`
   - how to start the frontend from `frontend/`
   - any required environment variables, referring only to `.env.example`
   - that `data/campus_customs.db` and `data/products/` are local-only and are not included in the repository
7. Create/update `hw4/.gitignore` so it excludes:
   `.env`
   `.env.*`
   `!.env.example`
   `data/campus_customs.db`
   `data/products/`
   `data/*.zip`
   `data/yale_som_classes.json`
   `node_modules/`
   `dist/`
   `.venv/`
   `__pycache__/`
   `.DS_Store`
8. Do NOT copy the local data pack into the GitHub submission. In particular, do not include:
   - `data/campus_customs.db`
   - `data/products/`
   - any real `.env`
   - API keys or other secrets
9. Review `AI_prompts.md`. It currently contains a test email/password from an earlier assignment prompt. Do not expose any real credential. If it is clearly a fictional/test credential required to document the assignment, leave it; otherwise replace/redact it appropriately without changing the substance of the AI prompt history.
10. Preserve all completed Problem 12 work, including:

- `backend/audit.py`
- `backend/prompts/prompt.md`
- `output/audit_trail.json`
- `output/harness.md`

11. Preserve all three Problem 11 screenshots and make sure `output/app_check.html` still correctly references:

- `app_check_images/check-1.png`
- `app_check_images/check-2.png`
- `app_check_images/check-3.png`

12. Do not modify the functioning application logic unless necessary to make the new frontend location work.
13. Do not commit, push, or create a GitHub repository yet.

After making the packaging changes, verify the resulting structure and report:

- the final `hw4/` tree
- what files were created or moved
- that no database, product images, `.env`, or API keys are inside the submission
- that the frontend still builds
- that the backend still imports/compiles
- any issue that remains before we commit and push.

### 3. Corrections needed in the first prompt

_To be determined._

