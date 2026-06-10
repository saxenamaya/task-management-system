import { useState } from "react";

import {
  Button,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import api from "../api/api";

export default function CreateRulePage() {
  const [taskId, setTaskId] = useState("");
  const [department, setDepartment] = useState("QA");
  const [minExperience, setMinExperience] = useState("3");
  const [maxActiveTasks, setMaxActiveTasks] = useState("5");
  const [location, setLocation] = useState("Bangalore");

  const handleSubmit = async () => {
    try {
      const payload = {
        task_id: Number(taskId),
        department,
        min_experience: Number(minExperience),
        max_active_tasks: Number(maxActiveTasks),
        location,
      };

      const response = await api.post(
        "/task-rules",
        payload
      );

      alert(`Rule Created. ID = ${response.data.id}`);
    } catch (error) {
      console.error(error);
      alert("Rule Creation Failed");
    }
  };

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Create Rule
      </Typography>

      <TextField
        fullWidth
        margin="normal"
        label="Task ID"
        value={taskId}
        onChange={(e) => setTaskId(e.target.value)}
      />

      <TextField
        fullWidth
        margin="normal"
        label="Department"
        value={department}
        onChange={(e) => setDepartment(e.target.value)}
      />

      <TextField
        fullWidth
        margin="normal"
        label="Minimum Experience"
        value={minExperience}
        onChange={(e) => setMinExperience(e.target.value)}
      />

      <TextField
        fullWidth
        margin="normal"
        label="Max Active Tasks"
        value={maxActiveTasks}
        onChange={(e) => setMaxActiveTasks(e.target.value)}
      />

      <TextField
        fullWidth
        margin="normal"
        label="Location"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />

      <Button
        variant="contained"
        sx={{ mt: 2 }}
        onClick={handleSubmit}
      >
        Create Rule
      </Button>
    </Paper>
  );
}