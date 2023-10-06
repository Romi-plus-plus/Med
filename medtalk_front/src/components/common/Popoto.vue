<template>
  <section class="ppt-section-main">
    <div class="ppt-section-header">
      <span class="ppt-header-span">医疗问答知识图谱</span>
    </div>

    <div class="ppt-container-graph">
      <div id="popoto-taxonomy" class="ppt-taxo-nav"></div>

      <div class="my-ppt-container-results">
        <!-- Add a header with total number of results count -->
        <div class="ppt-section-header">
          RESULTS <span class="ppt-count">{{ rescount }}</span>
        </div>

        <div id="popoto-results" class="ppt-container-results">
          <!-- Results are generated here -->
        </div>
      </div>

      <!-- By default the graph is generated on the HTML element with ID "popoto-graph"
     If needed this id can be modified with property "popoto.graph.containerId" -->

      <div id="popoto-graph" class="ppt-div-graph">
        <!-- Graph is generated here -->
      </div>
    </div>
    <div class="ppt-container-bottom">
      <!-- By default the query viewer is generated on the HTML element with ID "popoto-query"
     If needed this id can be modified with property "popoto.queryviewer.containerId" -->

      <div id="popoto-query" class="ppt-container-query">
        <!-- Query viewer is generated here -->
      </div>

      <!-- By default the cypher viewer is generated on the HTML element with ID "popoto-cypher"
     If needed this id can be modified with property "popoto.cypherviewer.containerId" -->

      <div id="popoto-cypher" class="ppt-container-cypher">
        <!-- Cypher query viewer will be generated here -->
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import neo4j from "neo4j-driver";
import * as popoto from "popoto";

const driver = neo4j.driver(
  import.meta.env.VITE_NEO4J_URL,
  neo4j.auth.basic(import.meta.env.VITE_NEO4J_USERNAME, import.meta.env.VITE_NEO4J_PASSWORD)
);

popoto.runner.DRIVER = driver;
(popoto.graph.link as any).SHOW_MARKER = true;

// Activate the option to fit the text inside the nodes
popoto.graph.USE_FIT_TEXT = true;

// Add action in toolbar to toggle the fit text option
(popoto.tools as any).TOGGLE_FIT_TEXT = true;

// Change the number of displayed results:
(popoto.query as any).RESULTS_PAGE_SIZE = 25;

// Define the list of label provider to customize the graph behavior:
popoto.provider.node.Provider = {
  Check: {
    returnAttributes: ["name"],
  },
  Disease: {
    returnAttributes: [
      "name",
      "prevent",
      "easy_get",
      "cured_prob",
      "desc",
      "cure_lasttime",
      "cure_way",
      "cause",
      "cure_department",
    ],
  },
  Drug: {
    returnAttributes: ["name"],
  },
  Food: {
    returnAttributes: ["name"],
  },
  Symptom: {
    returnAttributes: ["name"],
  },
};

const rescount = ref(0);

// Add a listener on returned result count to update count in page
popoto.result.onTotalResultCount((count) => (rescount.value = count));

driver
  .verifyConnectivity()
  .then(function () {
    // Start the generation using parameter as root label of the query.
    popoto.start("Disease");
  })
  .catch(function (error: any) {
    console.error(error);
  });
</script>

<style lang="scss">
.ppt-icon.ppt-menu.fullscreen {
  position: initial;
  top: initial;
  left: initial;
  bottom: initial;
  right: initial;
}
.ppt-result {
  margin: 0;
  background-color: var(--q-primary-2);
  color: black;
  border: var(--q-primary-6) 1px solid;
  border-radius: 4px;
  border-collapse: collapse;
  &:hover {
    background-color: var(--q-primary-2);
  }
}
.ppt-count {
  color: var(--q-primary-8);
}
.ppt-result-attribute-div span {
  margin-right: 1em !important;
  &:nth-child(1) {
    color: var(--q-primary);
    font-weight: bold;
  }
  &:nth-child(2) {
    white-space: pre-wrap;
  }
}
.ppt-container-graph {
  background-color: #eee;
}
.ppt-header-span {
  color: var(--q-primary);
}
.ppt-section-header {
  margin-top: 0;
  color: var(--q-primary-10);
  background-color: var(--q-primary-3);
}
.ppt-taxo-nav {
  background-color: var(--q-primary-2);
}
.ppt-taxo__span-icon:before {
  color: var(--q-primary);
}
.ppt-taxo-li + .ppt-taxo-li {
  margin-top: 4px;
}
.ppt-label {
  background-color: var(--q-primary-3);
  border-radius: 4px;
  padding: 2px 4px;
  &:hover {
    color: var(--q-primary-6);
  }
}
.ppt-div-graph {
  background-color: var(--q-primary-1);
}
.my-ppt-container-results {
  float: right;
  max-width: 400px;
  text-align: justify;
  .ppt-section-header {
    margin-top: 0;
    background-color: var(--q-primary-4);
  }
}
.ppt-container-results {
  background-color: #eee;
  max-height: calc(100vh - 190px);
}
.ppt-container-query,
.ppt-container-cypher {
  background-color: var(--q-primary-2);
  .ppt-span {
    color: var(--q-primary-8);
  }
}

.ppt-container-graph {
  height: calc(100vh - 150px);
}

.ppt-section-header {
  height: 40px;
  line-height: 40px;
}

.ppt-container-query,
.ppt-container-cypher {
  margin-top: 0;
  position: relative;
  height: 30px;
  line-height: 30px;
  padding: 0;
  border: var(--q-primary-6) 1px solid;
  border-radius: 4px;
  border-collapse: collapse;
}
</style>
