import { useState } from "react";

import {
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import api from "../api/api";

export default function EligibleTasksPage() {
  const [userId, setUserId] = useState("");
  const [result, setResult] = useState<any>(null);

  const handleFetch = async () => {
    try {
      const response = await api.get(
        `/users/${userId}/eligible-tasks`
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to load tasks");
    }
  };

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Eligible Tasks
      </Typography>

      <TextField
        fullWidth
        margin="normal"
        label="User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />

      <Button
        variant="contained"
        sx={{ mt: 2 }}
        onClick={handleFetch}
      >
        Get Eligible Tasks
      </Button>

      {result && (
        <>
          <Typography sx={{ mt: 4, mb: 2 }}>
            Task Count: {result.count}
          </Typography>

          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Title</TableCell>
                <TableCell>Priority</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {result.eligible_tasks.map((task: any) => (
                <TableRow key={task.id}>
                  <TableCell>{task.id}</TableCell>
                  <TableCell>{task.title}</TableCell>
                  <TableCell>{task.priority}</TableCell>
                  <TableCell>{task.status}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </>
      )}
    </Paper>
  );
}