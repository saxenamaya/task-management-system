import {
  AppBar,
  Box,
  Button,
  Drawer,
  List,
  ListItemButton,
  ListItemText,
  Toolbar,
  Typography,
} from "@mui/material";

import { Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.tsx";

const drawerWidth = 240;

export default function DashboardLayout() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  return (
    <Box sx={{ display: "flex" }}>
      <AppBar
        position="fixed"
        sx={{
          zIndex: 1201,
        }}
      >
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Task Management System
          </Typography>

          <Button
            color="inherit"
            onClick={() => {
              logout();
            }}
          >
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar />

        <List>
          <ListItemButton onClick={() => navigate("/")}>
            <ListItemText primary="Dashboard" />
          </ListItemButton>

          <ListItemButton onClick={() => navigate("/tasks/create")}>
            <ListItemText primary="Create Task" />
          </ListItemButton>

          <ListItemButton onClick={() => navigate("/rules/create")}>
            <ListItemText primary="Create Rule" />
          </ListItemButton>

          <ListItemButton onClick={() => navigate("/eligible-users")}>
            <ListItemText primary="Eligible Users" />
          </ListItemButton>

          <ListItemButton onClick={() => navigate("/eligible-tasks")}>
            <ListItemText primary="Eligible Tasks" />
          </ListItemButton>
        </List>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
        }}
      >
        <Toolbar />

        <Outlet />
      </Box>
    </Box>
  );
}
