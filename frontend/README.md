# Frontend

The frontend is the operator dashboard for Agent Activity. It is built with Angular and gives the backend data a usable interface: agents become searchable records, metrics become charts and cards, screenshots become browsable evidence, and command results become something an operator can actually inspect without touching the API directly.

![Home page](../assets/frontend/home-page.png)

## Running It Locally

Start the backend first so the dashboard has an API to call. Then run:

```sh
npm install
ng serve
```

The app opens at `http://localhost:4200`. In development it calls `http://localhost:8000`, configured in `src/environments/environment.ts`. The production environment uses `/api`, which is useful when the dashboard and API are served behind the same reverse proxy.

## What The Dashboard Covers

The home page summarizes the current fleet state, including total agents, online agents, offline agents, and recently seen machines. The agents area is the main workflow: from the list you can filter machines, open a detail page, inspect system information, review recent metrics, and navigate into activity specific views.

Agent detail pages connect the related views together: metrics, clipboards, keylogs, screenshots, and commands. The global clipboards, keylogs, and screenshots pages are useful when you want to search or review activity across agents instead of starting from a single machine.
