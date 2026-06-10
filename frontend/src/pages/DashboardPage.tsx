import { useEffect, useState } from "react";

import {
  Card,
  CardContent,
  Grid,
  Typography,
} from "@mui/material";

import api from "../api/api.ts";

interface DashboardStats {
  tasks: number;
  rules: number;
  eligible_users: number;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    tasks: 0,
    rules: 0,
    eligible_users: 0,
  });

  useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await api.get("/dashboard/stats");
        setStats(response.data);
      } catch (error) {
        console.error("Failed to load dashboard stats", error);
      }
    };

    loadStats();
  }, []);

  return (
    <>
      <Typography variant="h3" gutterBottom>
        Dashboard
      </Typography>

      <Typography sx={{ mb: 4 }}>
        Welcome to Task Management System
      </Typography>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography
                color="text.secondary"
                gutterBottom
              >
                Total Tasks
              </Typography>

              <Typography variant="h3">
                {stats.tasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography
                color="text.secondary"
                gutterBottom
              >
                Rules
              </Typography>

              <Typography variant="h3">
                {stats.rules}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography
                color="text.secondary"
                gutterBottom
              >
                Eligible Assignments
              </Typography>

              <Typography variant="h3">
                {stats.eligible_users}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </>
  );
}