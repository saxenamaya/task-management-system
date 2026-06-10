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

export default function EligibleUsersPage() {
  const [taskId, setTaskId] = useState("");
  const [result, setResult] = useState<any>(null);

  const handleCompute = async () => {
    try {
      await api.post(
        `/tasks/${taskId}/compute-eligibility`
      );

      const response = await api.get(
        `/tasks/${taskId}/eligible-users`
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to compute eligibility");
    }
  };

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Eligible Users
      </Typography>

      <TextField
        fullWidth
        margin="normal"
        label="Task ID"
        value={taskId}
        onChange={(e) => setTaskId(e.target.value)}
      />

      <Button
        variant="contained"
        sx={{ mt: 2 }}
        onClick={handleCompute}
      >
        Compute Eligibility
      </Button>

      {result && (
        <>
          <Typography sx={{ mt: 4, mb: 2 }}>
            Eligible Users Count: {result.count}
          </Typography>

          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Department</TableCell>
                <TableCell>Experience</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Active Tasks</TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {result.eligible_users.map((user: any) => (
                <TableRow key={user.id}>
                  <TableCell>{user.id}</TableCell>
                  <TableCell>{user.name}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.department}</TableCell>
                  <TableCell>{user.experience_years}</TableCell>
                  <TableCell>{user.location}</TableCell>
                  <TableCell>{user.active_task_count}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </>
      )}
    </Paper>
  );
}