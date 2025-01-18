<template>
  <div id="app" class="container">
    <header class="app-header">
      <h1>Traffic Flow Optimizer</h1>
    </header>

    <main class="main-content">
      <div class="dropdown-container">
        <div class="dropdown">
          <label for="by-date">Select File by Date:</label>
          <select id="by-date" v-model="selectedByDate" @change="changeMiniGraph(selectedByDate)">
            <option v-for="file in filesByDate" :key="file" :value="file">
              {{ file }}
            </option>
          </select>
        </div>

        <div class="dropdown">
          <label for="by-time">Select File by Time:</label>
          <select id="by-time" v-model="selectedByTime" @change="changeMiniGraph(selectedByTime)">
            <option v-for="file in filesByTime" :key="file" :value="file">
              {{ file }}
            </option>
          </select>
        </div>

        <div class="dropdown">
          <label for="by-month">Select File by Month:</label>
          <select id="by-month" v-model="selectedByMonth" @change="changeMiniGraph(selectedByMonth)">
            <option v-for="file in filesByMonth" :key="file" :value="file">
              {{ file }}
            </option>
          </select>
        </div>
      </div>

      <button class="optimize-button" @click="optimize">Optimize Traffic</button>
    </main>

    <footer class="app-footer">
      <p>&copy; 2025 Traffic Flow Optimization System</p>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filesByDate: [],
      filesByTime: [],
      filesByMonth: [],
      selectedByDate: "",
      selectedByTime: "",
      selectedByMonth: "",
    };
  },
  methods: {
    async fetchFiles(endpoint, targetArray) {
      try {
        const response = await fetch(endpoint);
        const files = await response.json();
        this[targetArray] = files;
      } catch (error) {
        console.error(`Error fetching ${targetArray}:`, error);
      }
    },
    async changeMiniGraph(fileName) {
      try {
        const response = await fetch(`/api/change-mini-graph?file=${fileName}`, {
          method: "POST",
        });
        const result = await response.json();
        console.log("Mini graph updated:", result);
      } catch (error) {
        console.error("Error updating mini graph:", error);
      }
    },
    async optimize() {
      try {
        const response = await fetch("/api/optimize", {
          method: "POST",
        });
        const result = await response.json();
        console.log("Optimization result:", result);
      } catch (error) {
        console.error("Error optimizing:", error);
      }
    },
  },
  mounted() {
    this.fetchFiles("by-date", "filesByDate");
    this.fetchFiles("by-time", "filesByTime");
    this.fetchFiles("by-month", "filesByMonth");
  },
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f9;
  color: #333;
}

.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  background-color: #007bff;
  color: white;
  text-align: center;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1.5rem;
}

.dropdown-container {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.dropdown {
  display: flex;
  flex-direction: column;
  align-items: start;
  gap: 0.5rem;
}

.dropdown select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.optimize-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.optimize-button:hover {
  background-color: #0056b3;
}

.app-footer {
  text-align: center;
  padding: 1rem;
  background-color: #f4f4f9;
  font-size: 0.9rem;
  color: #666;
  border-top: 1px solid #ddd;
}
</style>
