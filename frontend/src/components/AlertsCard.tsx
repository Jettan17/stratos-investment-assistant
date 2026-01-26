"use client";

import { useState, useEffect } from "react";
import type { Alert, AlertCreate, AlertCheck, AlertType } from "@/lib/api";
import { getAlerts, createAlert, deleteAlert, checkAlerts } from "@/lib/api";

function formatCurrency(value: number | null): string {
  if (value === null || value === undefined) return "N/A";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
}

function getAlertTypeLabel(type: AlertType): string {
  switch (type) {
    case "price_above":
      return "Price Above";
    case "price_below":
      return "Price Below";
    case "percent_change":
      return "% Change";
    default:
      return type;
  }
}

function getAlertStatusColor(alert: Alert): string {
  if (!alert.is_active) return "text-slate-500";
  if (alert.is_triggered) return "text-green-400";
  return "text-yellow-400";
}

function getAlertStatusLabel(alert: Alert): string {
  if (!alert.is_active) return "Inactive";
  if (alert.is_triggered) return "Triggered";
  return "Watching";
}

export default function AlertsCard() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [alertChecks, setAlertChecks] = useState<AlertCheck[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newAlert, setNewAlert] = useState<AlertCreate>({
    symbol: "",
    alert_type: "price_above",
    target_value: 0,
  });

  const fetchAlerts = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getAlerts(false); // Get all alerts
      setAlerts(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load alerts");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCheckAlerts = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const checks = await checkAlerts();
      setAlertChecks(checks);
      // Refresh alerts to get updated trigger status
      await fetchAlerts();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to check alerts");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const handleAddAlert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAlert.symbol || newAlert.target_value <= 0) {
      return;
    }

    try {
      await createAlert(newAlert);
      setNewAlert({ symbol: "", alert_type: "price_above", target_value: 0 });
      setShowAddForm(false);
      fetchAlerts();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create alert");
    }
  };

  const handleDeleteAlert = async (alertId: number) => {
    if (!confirm("Are you sure you want to delete this alert?")) return;

    try {
      await deleteAlert(alertId);
      fetchAlerts();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete alert");
    }
  };

  if (isLoading && alerts.length === 0) {
    return (
      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-400"></div>
          <span className="ml-3 text-slate-400">Loading alerts...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold text-slate-200">Price Alerts</h3>
        <div className="flex gap-2">
          <button
            onClick={handleCheckAlerts}
            disabled={isLoading}
            className="text-sm bg-cyan-600 hover:bg-cyan-700 disabled:bg-slate-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            {isLoading ? "Checking..." : "Check Now"}
          </button>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="text-sm bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            {showAddForm ? "Cancel" : "+ New Alert"}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/30 border border-red-700 rounded-lg text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* Triggered Alerts Notification */}
      {alertChecks.filter((c) => c.should_trigger).length > 0 && (
        <div className="mb-4 p-4 bg-green-900/30 border border-green-700 rounded-lg">
          <h4 className="text-green-400 font-medium mb-2">Triggered Alerts</h4>
          <ul className="space-y-1">
            {alertChecks
              .filter((c) => c.should_trigger)
              .map((check) => (
                <li key={check.alert.id} className="text-sm text-green-300">
                  {check.message}
                </li>
              ))}
          </ul>
        </div>
      )}

      {/* Add Alert Form */}
      {showAddForm && (
        <form onSubmit={handleAddAlert} className="mb-6 p-4 bg-slate-800 rounded-lg">
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm text-slate-400 mb-1">Symbol</label>
              <input
                type="text"
                value={newAlert.symbol}
                onChange={(e) =>
                  setNewAlert({ ...newAlert, symbol: e.target.value.toUpperCase() })
                }
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white"
                placeholder="AAPL"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Alert Type</label>
              <select
                value={newAlert.alert_type}
                onChange={(e) =>
                  setNewAlert({
                    ...newAlert,
                    alert_type: e.target.value as AlertType,
                  })
                }
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white"
              >
                <option value="price_above">Price Above</option>
                <option value="price_below">Price Below</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">
                Target Price
              </label>
              <input
                type="number"
                value={newAlert.target_value || ""}
                onChange={(e) =>
                  setNewAlert({
                    ...newAlert,
                    target_value: parseFloat(e.target.value) || 0,
                  })
                }
                className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white"
                placeholder="150.00"
                step="0.01"
                min="0"
                required
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            Create Alert
          </button>
        </form>
      )}

      {/* Alerts Table */}
      {alerts.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-700 text-slate-400">
                <th className="py-2 px-3">Symbol</th>
                <th className="py-2 px-3">Type</th>
                <th className="py-2 px-3 text-right">Target</th>
                <th className="py-2 px-3 text-center">Status</th>
                <th className="py-2 px-3 text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((alert) => (
                <tr
                  key={alert.id}
                  className="border-b border-slate-800 hover:bg-slate-800/50"
                >
                  <td className="py-2 px-3 font-semibold text-primary-400">
                    {alert.symbol}
                  </td>
                  <td className="py-2 px-3 text-slate-300">
                    {getAlertTypeLabel(alert.alert_type)}
                  </td>
                  <td className="py-2 px-3 text-right text-slate-200">
                    {formatCurrency(alert.target_value)}
                  </td>
                  <td
                    className={`py-2 px-3 text-center ${getAlertStatusColor(alert)}`}
                  >
                    {getAlertStatusLabel(alert)}
                  </td>
                  <td className="py-2 px-3 text-center">
                    <button
                      onClick={() => handleDeleteAlert(alert.id)}
                      className="text-red-400 hover:text-red-300 transition-colors"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-8 text-slate-400">
          <p className="text-lg">No alerts set up yet.</p>
          <p className="text-sm mt-2">
            Create an alert to get notified when a stock hits your target price.
          </p>
        </div>
      )}
    </div>
  );
}
