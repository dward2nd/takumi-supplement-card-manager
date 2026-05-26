import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { AppContext, useAppStore } from "./data/state";
import { Layout } from "./components/Layout";
import { LoginScreen } from "./screens/LoginScreen";
import { HomeScreen } from "./screens/HomeScreen";
import { CardsScreen } from "./screens/CardsScreen";
import { CardDetailScreen } from "./screens/CardDetailScreen";
import { TransactionsHistoryScreen } from "./screens/TransactionsHistoryScreen";
import { BillsScreen } from "./screens/BillsScreen";
import { BillsHistoryScreen } from "./screens/BillsHistoryScreen";
import { BillDetailScreen } from "./screens/BillDetailScreen";
import { AddTransactionScreen } from "./screens/AddTransactionScreen";
import { SettingsScreen } from "./screens/SettingsScreen";

function App() {
  const store = useAppStore();
  return (
    <AppContext.Provider value={store}>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<RootGate />} />
          <Route path="/login" element={<LoginScreen />} />
          <Route
            path="/home"
            element={
              <Guard>
                <HomeScreen />
              </Guard>
            }
          />
          <Route
            path="/cards"
            element={
              <Guard>
                <CardsScreen />
              </Guard>
            }
          />
          <Route
            path="/cards/:id"
            element={
              <Guard>
                <CardDetailScreen />
              </Guard>
            }
          />
          <Route
            path="/cards/:id/history"
            element={
              <Guard>
                <TransactionsHistoryScreen />
              </Guard>
            }
          />
          <Route
            path="/bills"
            element={
              <Guard>
                <BillsScreen />
              </Guard>
            }
          />
          <Route
            path="/bills/history"
            element={
              <Guard>
                <BillsHistoryScreen />
              </Guard>
            }
          />
          <Route
            path="/bills/:id"
            element={
              <Guard>
                <BillDetailScreen />
              </Guard>
            }
          />
          <Route
            path="/add"
            element={
              <Guard>
                <AddTransactionScreen />
              </Guard>
            }
          />
          <Route
            path="/settings"
            element={
              <Guard>
                <SettingsScreen />
              </Guard>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </AppContext.Provider>
  );
}

const RootGate = () => {
  const store = useAppStore();
  // The state from this hook is independent of the provider — read directly
  // for the initial routing decision.
  if (store.holderKey) return <Navigate to="/home" replace />;
  return <LoginScreen />;
};

const Guard = ({ children }: { children: React.ReactNode }) => {
  const loc = useLocation();
  // Use the localStorage key directly to survive the brief moment before context settles.
  const v = typeof window !== "undefined" ? window.localStorage.getItem("takumi.poc.holder") : null;
  if (!v) return <Navigate to="/" replace state={{ from: loc }} />;
  return <>{children}</>;
};

export default App;
