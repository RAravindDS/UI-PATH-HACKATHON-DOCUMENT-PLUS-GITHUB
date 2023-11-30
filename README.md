# PDFInsightHub

## Aim for the project - 
*Adding features to the Ui Path Document Understanding*

**Developers can do complex queries to graph, text and tables. The goal of this project is to make it easy for users to explore and analyze both structured and unstructured data. We aim to provide a user-friendly tool that simplifies data understanding, helping users make informed decisions and gain insights effortlessly.**

## Architecture

**Credit goes to RepoReel**❤️
#### Overall Workflow
```
  ┌─────────────────┐         ┌─────────────────┐          ┌─────────────────┐
  │                 │         │                 │          │    imgs_pdfs    │
  │ User/Developer  │────────►│    UI-PATH      │─────────►│(Sample Data for │
  │                 │  Set up │   HACKATHON     │ Process  │ processing and  │
  └─────────────────┘         │   DOCUMENT      │   and    │     analysis)   │
                              │     PLUS        │ Analyze  └─────────────────┘
 ┌─────────────────┐          │   GITHUB App    │          ┌─────────────────┐
 │.gitignore & .env│          │                 │          │    research     │
 ├─────────────────┤          └─────────────────┘          │(Research scripts,│
 │Requirements.txt │                                       │ notes, data etc.)│
 └─────────────────┘                                       └─────────────────┘
(Setup and config  )                                       
(files)                                                      
```
#### Folder structure 
```


                            [ Repository: UI-PATH-HACKATHON-DOCUMENT-PLUS-GITHUB ]
                                        /
                      .---------------------------------------------------------.
                      |                    |                    |               |
                  [ App 1 ]            [ App 2 ]            [ App 3 ]       [ Shared ]
                      |                    |                    |            Resources
                      |                    |                    |               |
      .-------------------------.  .-------------------------.  .-------------------------.
      | - .env                  |  | - .env                  |  | - .env                  |
      | - requirements.txt      |  | - requirements.txt      |  | - requirements.txt      |
      | - App-specific src      |  | - App-specific src      |  | - App-specific src      |
      | - Documentation         |  | - Documentation         |  | - Documentation         |
      | - imgs_pdfs (if used)   |  | - imgs_pdfs (if used)   |  | - imgs_pdfs (if used)   |
      | - research (if used)    |  | - research (if used)    |  | - research (if used)    |
      '-------------------------'  '-------------------------'  '-------------------------'

Legend: [ ] - Component
        -   - Component's sub-items

```

## Key features

**1.Knowledge Graph :**

-  Upload PDFs: Seamlessly upload your PDF documents.
-  Dynamic Knowledge Graphs: Watch as the app converts document content into dynamic knowledge graphs.
-  Query Engine: Ask complex questions and receive insights from the structured knowledge.

  
.**2.Graph Query:**

-  Graphical Data Extraction: Identify and extract all graphs and charts from your documents.
-  Interactive Exploration: Query and analyze graphical data with ease.
-  Visual Insights: Gain valuable insights from your data visualizations.

  
.**3.Table Query:**

-  Table Recognition: Extract and organize tabular data from PDFs.
-  Effortless Queries: Seamlessly query and filter tabular information.
-  Data Precision: Get precise answers from your document's structured tables.


======= \
Problem statement 2 - [RepoReel](www.google.com)
