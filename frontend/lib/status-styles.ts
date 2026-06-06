export type GEPanelStatus = "planned" | "completed" | "in_progress";

export const GE_STATUS_ORDER = ["planned", "in_progress", "completed"] as const;

export const GE_STATUS_LABELS: Record<GEPanelStatus, string> = {
  planned: "Plan",
  completed: "Done",
  in_progress: "IP",
};

export const GE_STATUS_STYLES: Record<GEPanelStatus, {
  activeButton: string;
  inactiveButton: string;
  selectedCard: string;
  selectedRow: string;
  selectedTitle: string;
  selectedText: string;
  selectedSubtleText: string;
}> = {
  planned: {
    activeButton: "border-blue-600 bg-blue-600 text-white",
    inactiveButton: "border-blue-200 text-blue-700 hover:border-blue-400 hover:bg-blue-50",
    selectedCard: "border-blue-200 bg-blue-50",
    selectedRow: "border-blue-300 bg-blue-50/40",
    selectedTitle: "text-blue-900",
    selectedText: "text-blue-800/80",
    selectedSubtleText: "text-blue-800/70",
  },
  completed: {
    activeButton: "border-green-700 bg-green-700 text-white",
    inactiveButton: "border-green-200 text-green-800 hover:border-green-400 hover:bg-green-50",
    selectedCard: "border-green-200 bg-green-50",
    selectedRow: "border-green-300 bg-green-50/40",
    selectedTitle: "text-green-900",
    selectedText: "text-green-800/80",
    selectedSubtleText: "text-green-800/70",
  },
  in_progress: {
    activeButton: "border-orange-600 bg-orange-600 text-white",
    inactiveButton: "border-orange-200 text-orange-700 hover:border-orange-400 hover:bg-orange-50",
    selectedCard: "border-orange-200 bg-orange-50",
    selectedRow: "border-orange-300 bg-orange-50/40",
    selectedTitle: "text-orange-900",
    selectedText: "text-orange-800/80",
    selectedSubtleText: "text-orange-800/70",
  },
};
