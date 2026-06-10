import { useState } from "react";
import {
  Button,
  Card,
  Container,
  TextField,
  Typography,
} from "@mui/material";

import api from "../api/api.ts";
import { useAuth } from "../context/AuthContext.tsx";

export default function LoginPage() {
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const form = new URLSearchParams();

      form.append("username", email);
      form.append("password", password);

      const response = await api.post(
        "/auth/login",
        form,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      login(response.data.access_token);

      alert("Login Successful");
    } catch (error) {
      console.error(error);
      alert("Login Failed");
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 10 }}>
      <Card sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Task Management System
        </Typography>

        <TextField
          fullWidth
          margin="normal"
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <TextField
          fullWidth
          margin="normal"
          type="password"
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <Button
          variant="contained"
          fullWidth
          sx={{ mt: 2 }}
          onClick={handleLogin}
        >
          Login
        </Button>
      </Card>
    </Container>
  );
}
