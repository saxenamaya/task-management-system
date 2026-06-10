import { useState } from "react";

import {
  Button,
  MenuItem,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import api from "../api/api";

export default function CreateTaskPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const [priority, setPriority] = useState("MEDIUM");

  const [status, setStatus] = useState("TODO");

  const [createdBy, setCreatedBy] = useState("1");

  const handleSubmit = async () => {
    try {
      const payload = {
        title,
        description,
        priority,
        status,
        created_by: Number(createdBy),
      };

      const response = await api.post("/tasks", payload);

      alert(`Task Created. ID = ${response.data.id}`);

      setTitle("");
      setDescription("");
    } catch (error) {
      console.error(error);
      alert("Task Creation Failed");
    }
  };

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Create Task
      </Typography>

      <TextField
        fullWidth
        margin="normal"
        label="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <TextField
        fullWidth
        multiline
        rows={4}
        margin="normal"
        label="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <TextField
        select
        fullWidth
        margin="normal"
        label="Priority"
        value={priority}
        onChange={(e) => setPriority(e.target.value)}
      >
        <MenuItem value="LOW">LOW</MenuItem>
        <MenuItem value="MEDIUM">MEDIUM</MenuItem>
        <MenuItem value="HIGH">HIGH</MenuItem>
      </TextField>

      <TextField
        select
        fullWidth
        margin="normal"
        label="Status"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
      >
        <MenuItem value="TODO">TODO</MenuItem>
        <MenuItem value="IN_PROGRESS">IN_PROGRESS</MenuItem>
        <MenuItem value="DONE">DONE</MenuItem>
      </TextField>

      <TextField
        fullWidth
        margin="normal"
        label="Created By User ID"
        value={createdBy}
        onChange={(e) => setCreatedBy(e.target.value)}
      />

      <Button
        variant="contained"
        sx={{ mt: 2 }}
        onClick={handleSubmit}
      >
        Create Task
      </Button>
    </Paper>
  );
}