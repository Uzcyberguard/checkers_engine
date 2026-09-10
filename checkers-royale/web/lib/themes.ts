/**
 * Board palettes sampled pixel-for-pixel from the board art in the original
 * checkers_engine repository, so the web build keeps the same look while
 * rendering everything as crisp CSS instead of a fixed-size PNG.
 */

export interface Theme {
  id: string;
  name: string;
  light: string;
  dark: string;
  frame: string;
  frameEdge: string;
  label: string;
  accent: string;
  /** [highlight, base, shade] for the light army's discs. */
  pieceLight: [string, string, string];
  pieceDark: [string, string, string];
  crownLight: string;
  crownDark: string;
}

const IVORY: [string, string, string] = ["#fffdf7", "#efe7d5", "#bdb098"];
const CHARCOAL: [string, string, string] = ["#5c5f66", "#2a2d34", "#111318"];
const CRIMSON: [string, string, string] = ["#e0554f", "#a8272a", "#5e1114"];
const ESPRESSO: [string, string, string] = ["#6b4a33", "#3d271a", "#1c110a"];

export const THEMES: Theme[] = [
  {
    id: "emerald",
    name: "Emerald & Ivory",
    light: "#f5f0e1",
    dark: "#4a7c59",
    frame: "#1c2e26",
    frameEdge: "#2c453a",
    label: "#d6b26e",
    accent: "#e8c27a",
    pieceLight: IVORY,
    pieceDark: CHARCOAL,
    crownLight: "#c9a24a",
    crownDark: "#e8c27a",
  },
  {
    id: "navy",
    name: "Navy & Gold",
    light: "#eee7d5",
    dark: "#3d5a80",
    frame: "#182038",
    frameEdge: "#27324f",
    label: "#d4af64",
    accent: "#e6c076",
    pieceLight: IVORY,
    pieceDark: CHARCOAL,
    crownLight: "#c9a24a",
    crownDark: "#e6c076",
  },
  {
    id: "burgundy",
    name: "Burgundy & Cream",
    light: "#f0e8d8",
    dark: "#823237",
    frame: "#2e1418",
    frameEdge: "#462226",
    label: "#d2b482",
    accent: "#e2be86",
    pieceLight: IVORY,
    pieceDark: ESPRESSO,
    crownLight: "#b8873c",
    crownDark: "#e2be86",
  },
  {
    id: "walnut",
    name: "Maple & Walnut",
    light: "#e8c89a",
    dark: "#7a4e2b",
    frame: "#4a2c18",
    frameEdge: "#61391f",
    label: "#e6cda0",
    accent: "#f0d6a8",
    pieceLight: IVORY,
    pieceDark: CRIMSON,
    crownLight: "#b8873c",
    crownDark: "#f4d79a",
  },
  {
    id: "teal",
    name: "Charcoal & Teal",
    light: "#dfe4e1",
    dark: "#2a6e6e",
    frame: "#1e1e22",
    frameEdge: "#2e2e34",
    label: "#bed2cd",
    accent: "#8fd6cc",
    pieceLight: IVORY,
    pieceDark: CHARCOAL,
    crownLight: "#c9a24a",
    crownDark: "#8fd6cc",
  },
  {
    id: "forest",
    name: "Deep Forest",
    light: "#e8e2ca",
    dark: "#225233",
    frame: "#102016",
    frameEdge: "#1d3626",
    label: "#c8b982",
    accent: "#d8c88c",
    pieceLight: IVORY,
    pieceDark: ESPRESSO,
    crownLight: "#b8873c",
    crownDark: "#d8c88c",
  },
  {
    id: "copper",
    name: "Indigo & Copper",
    light: "#f5ebdb",
    dark: "#b0623e",
    frame: "#1e1830",
    frameEdge: "#2e2547",
    label: "#e0b080",
    accent: "#f0c090",
    pieceLight: IVORY,
    pieceDark: CHARCOAL,
    crownLight: "#c9a24a",
    crownDark: "#f0c090",
  },
  {
    id: "oak",
    name: "Aged Oak",
    light: "#d5ac75",
    dark: "#573319",
    frame: "#30190b",
    frameEdge: "#45250f",
    label: "#ebd7af",
    accent: "#f2dcb4",
    pieceLight: IVORY,
    pieceDark: CRIMSON,
    crownLight: "#b8873c",
    crownDark: "#f2dcb4",
  },
];

export const DEFAULT_THEME = THEMES[0];

export function themeById(id: string): Theme {
  return THEMES.find((theme) => theme.id === id) ?? DEFAULT_THEME;
}
