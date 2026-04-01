const POSITIONS = ["X", "SL", "TE", "C", "QB", "RB", "Z"];

const POS_COLORS = {
  X: "#3b82f6",
  SL: "#3b82f6",
  TE: "#22c55e",
  C: "#22d3ee",
  QB: "#f0b429",
  RB: "#f97316",
  Z: "#a855f7",
};

const ROUTE_COLORS = {
  route: "#3b82f6",
  run: "#f97316",
  block: "#22d3ee",
};

const FORMATIONS = {
  BASE: {
    id: "BASE",
    label: "Base",
    tabClass: "base",
    positions: {
      X: { x: 0.14, y: 0.62 },
      SL: { x: 0.30, y: 0.70 },
      TE: { x: 0.42, y: 0.62 },
      C: { x: 0.50, y: 0.62 },
      QB: { x: 0.50, y: 0.74 },
      RB: { x: 0.50, y: 0.87 },
      Z: { x: 0.86, y: 0.62 },
    },
  },
  BOXL: {
    id: "BOXL",
    label: "Box Left",
    tabClass: "boxl",
    positions: {
      X: { x: 0.18, y: 0.62 },
      TE: { x: 0.28, y: 0.62 },
      Z: { x: 0.38, y: 0.62 },
      C: { x: 0.50, y: 0.62 },
      QB: { x: 0.50, y: 0.74 },
      SL: { x: 0.24, y: 0.72 },
      RB: { x: 0.32, y: 0.82 },
    },
  },
  GUN: {
    id: "GUN",
    label: "Gun",
    tabClass: "gun",
    positions: {
      X: { x: 0.16, y: 0.62 },
      TE: { x: 0.36, y: 0.62 },
      C: { x: 0.50, y: 0.62 },
      Z: { x: 0.66, y: 0.62 },
      QB: { x: 0.50, y: 0.76 },
      RB: { x: 0.60, y: 0.76 },
      SL: { x: 0.78, y: 0.70 },
    },
  },
};

function p(x, y) {
  return { x, y };
}

function line(base, pts) {
  return pts.map((pt) => ({ x: pt.x, y: pt.y }));
}

function withAssignments(basePlayers, assigns) {
  return POSITIONS.map((label) => ({
    label,
    color: POS_COLORS[label],
    x: basePlayers[label].x,
    y: basePlayers[label].y,
    rt: assigns[label].rt,
    route: assigns[label].route,
    mr: assigns[label].mr || null,
    a: assigns[label].a,
    roleName: assigns[label].roleName,
  }));
}

function passCall(formation, playName, names) {
  return `${formation} ${playName} — X ${names.X}, SL ${names.SL}, TE ${names.TE}, C ${names.C}, Z ${names.Z}, RB ${names.RB}`;
}

function formationPlayers(cat, assigns) {
  return withAssignments(FORMATIONS[cat].positions, assigns);
}

const PLAYS = [
  {
    id: "base-rb-left",
    cat: "BASE",
    category: "RUNNING",
    name: "RB Left",
    type: "run",
    tip: "RB presses north-south off center’s left hip. Wide players clear away from the run lane fast and stop clean.",
    passAt: null,
    passTo: null,
    hasMotion: false,
    motionPlayerLabel: null,
    motionType: null,
    call: passCall("Base", "RB Left", { X: "Hitch", SL: "Out", TE: "Delay", C: "Seal", Z: "Go", RB: "Dive Left" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.14, 0.53)]), a: "Push vertical five yards and settle away from the run lane.", roleName: "Hitch" },
      SL: { rt: "route", route: line("SL", [p(0.24, 0.67), p(0.19, 0.64)]), a: "Short out route left to widen support defenders.", roleName: "Out" },
      TE: { rt: "block", route: line("TE", [p(0.43, 0.58)]), a: "Show a short seal step then stop. No screening downfield.", roleName: "Seal" },
      C: { rt: "block", route: line("C", [p(0.48, 0.57)]), a: "Snap and work left hip leverage.", roleName: "Seal" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.72), p(0.48, 0.73)]), a: "Receive snap, open left, hand to RB, stay behind play.", roleName: "Open Left" },
      RB: { rt: "run", route: line("RB", [p(0.47, 0.78), p(0.46, 0.69), p(0.46, 0.52), p(0.46, 0.30)]), a: "Take handoff and hit vertical through the left A/B area.", roleName: "Dive Left" },
      Z: { rt: "route", route: line("Z", [p(0.86, 0.48), p(0.86, 0.34)]), a: "Clear backside vertically away from the run lane.", roleName: "Go" },
    }),
  },
  {
    id: "base-rb-right",
    cat: "BASE",
    category: "RUNNING",
    name: "RB Right",
    type: "run",
    tip: "Same aiming point to the other side. RB should stay vertical, not bounce outside.",
    passAt: null,
    passTo: null,
    hasMotion: false,
    motionPlayerLabel: null,
    motionType: null,
    call: passCall("Base", "RB Right", { X: "Go", SL: "Out", TE: "Seal", C: "Seal", Z: "Hitch", RB: "Dive Right" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.14, 0.48), p(0.14, 0.34)]), a: "Backside clear vertical route.", roleName: "Go" },
      SL: { rt: "route", route: line("SL", [p(0.34, 0.67), p(0.39, 0.64)]), a: "Short out to the right, widening the box.", roleName: "Out" },
      TE: { rt: "block", route: line("TE", [p(0.44, 0.58)]), a: "Show short seal right and stop.", roleName: "Seal" },
      C: { rt: "block", route: line("C", [p(0.52, 0.57)]), a: "Snap and help create right-side leverage.", roleName: "Seal" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.72), p(0.52, 0.73)]), a: "Receive snap, open right, place the ball, carry out fake.", roleName: "Open Right" },
      RB: { rt: "run", route: line("RB", [p(0.53, 0.78), p(0.54, 0.69), p(0.54, 0.52), p(0.54, 0.30)]), a: "Press north-south off the right hip of center.", roleName: "Dive Right" },
      Z: { rt: "route", route: line("Z", [p(0.86, 0.53)]), a: "Settle on a short hitch away from the vertical run lane.", roleName: "Hitch" },
    }),
  },
  {
    id: "base-screen-left",
    cat: "BASE",
    category: "RUNNING",
    name: "Screen Left",
    type: "pass",
    tip: "Sell vertical first, then throw quickly to the left with clean spacing.",
    passAt: 0.28,
    passTo: "SL",
    hasMotion: false,
    motionPlayerLabel: null,
    motionType: null,
    call: passCall("Base", "Screen Left", { X: "Stalk", SL: "Screen", TE: "Delay", C: "Snap", Z: "Clear", RB: "Check Release" }),
    players: formationPlayers("BASE", {
      X: { rt: "block", route: line("X", [p(0.14, 0.56)]), a: "Short step upfield, square to stalk the nearest flag puller.", roleName: "Stalk" },
      SL: { rt: "route", route: line("SL", [p(0.28, 0.71), p(0.21, 0.73), p(0.16, 0.71), p(0.12, 0.61)]), a: "Step back, show hands, then get upfield after the catch.", roleName: "Screen" },
      TE: { rt: "route", route: line("TE", [p(0.43, 0.56)]), a: "Delay and sit inside to hold support.", roleName: "Delay" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and settle. Do not drift illegally.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.73), p(0.47, 0.73)]), a: "Catch, open, and fire the screen fast.", roleName: "Quick Throw" },
      RB: { rt: "route", route: line("RB", [p(0.52, 0.80), p(0.58, 0.74), p(0.62, 0.68)]), a: "Check middle then release opposite to widen the defense.", roleName: "Check Release" },
      Z: { rt: "route", route: line("Z", [p(0.86, 0.48), p(0.86, 0.30)]), a: "Vertical clear route away from the screen action.", roleName: "Clear" },
    }),
  },
  {
    id: "base-orbit-sweep",
    cat: "BASE",
    category: "RUNNING",
    name: "Orbit Sweep",
    type: "run",
    tip: "Orbit motion should be smooth and early. QB rides the fake long enough to hold the edge defender.",
    passAt: null,
    passTo: null,
    hasMotion: true,
    motionPlayerLabel: "SL",
    motionType: "orbit",
    call: passCall("Base", "Orbit Sweep", { X: "Hitch", SL: "Orbit", TE: "Seal", C: "Snap", Z: "Clear", RB: "Fake Dive" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.14, 0.54)]), a: "Settle outside and be ready if play breaks.", roleName: "Hitch" },
      SL: { rt: "run", route: line("SL", [p(0.36, 0.78), p(0.56, 0.82), p(0.70, 0.72), p(0.78, 0.58), p(0.80, 0.42)]), mr: line("SL", [p(0.34, 0.76), p(0.44, 0.80), p(0.58, 0.81)]), a: "Orbit behind QB and take the handoff path around the backside.", roleName: "Orbit Sweep" },
      TE: { rt: "block", route: line("TE", [p(0.42, 0.57)]), a: "Short seal step to the left, stop on contact line.", roleName: "Seal" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and settle. Keep body under control.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.52, 0.74), p(0.56, 0.75)]), a: "Receive snap and mesh with orbit player.", roleName: "Ride Mesh" },
      RB: { rt: "run", route: line("RB", [p(0.49, 0.79), p(0.47, 0.66), p(0.47, 0.56)]), a: "Sell a hard inside fake to freeze middle support.", roleName: "Fake Dive" },
      Z: { rt: "route", route: line("Z", [p(0.86, 0.48), p(0.86, 0.30)]), a: "Vertical clear on the sweep side.", roleName: "Clear" },
    }),
  },
  {
    id: "base-hitch-go",
    cat: "BASE",
    category: "PASSING",
    name: "Hitch and Go",
    type: "pass",
    tip: "Sell the hitch with body language. QB holds the safety with eyes before launching.",
    passAt: 0.56,
    passTo: "X",
    hasMotion: false,
    motionPlayerLabel: null,
    motionType: null,
    call: passCall("Base", "Hitch and Go", { X: "Hitch-Go", SL: "Flat", TE: "Sit", C: "Snap", Z: "Post", RB: "Check" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.14, 0.54), p(0.14, 0.58), p(0.12, 0.40), p(0.10, 0.20)]), a: "Snap down into a hitch, then burst vertical.", roleName: "Hitch-Go" },
      SL: { rt: "route", route: line("SL", [p(0.22, 0.69), p(0.16, 0.70)]), a: "Quick flat route to occupy underneath help.", roleName: "Flat" },
      TE: { rt: "route", route: line("TE", [p(0.42, 0.56)]), a: "Sit inside as a safety valve.", roleName: "Sit" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and settle as the pocket anchor.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.72)]), a: "Three quick rhythm steps, eyes middle, then take the shot.", roleName: "Drop" },
      RB: { rt: "route", route: line("RB", [p(0.50, 0.81), p(0.56, 0.75)]), a: "Check protection lane then leak right.", roleName: "Check" },
      Z: { rt: "route", route: line("Z", [p(0.80, 0.48), p(0.66, 0.26)]), a: "Post route to pull the deep help defender.", roleName: "Post" },
    }),
  },
  {
    id: "base-all-go",
    cat: "BASE",
    category: "PASSING",
    name: "All Go",
    type: "pass",
    tip: "Great call versus aggressive corners. Keep spacing and let the QB choose the best one-on-one shot.",
    passAt: 0.48,
    passTo: "Z",
    hasMotion: false,
    motionPlayerLabel: null,
    motionType: null,
    call: passCall("Base", "All Go", { X: "Go", SL: "Seam", TE: "Seam", C: "Snap", Z: "Go", RB: "Swing" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.14, 0.46), p(0.14, 0.22)]), a: "Outside vertical.", roleName: "Go" },
      SL: { rt: "route", route: line("SL", [p(0.30, 0.56), p(0.30, 0.28)]), a: "Inside seam route.", roleName: "Seam" },
      TE: { rt: "route", route: line("TE", [p(0.42, 0.56), p(0.42, 0.31)]), a: "Tight seam release.", roleName: "Seam" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and hold center point.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.72)]), a: "Catch and throw with air to the best matchup.", roleName: "Drop" },
      RB: { rt: "route", route: line("RB", [p(0.56, 0.80), p(0.65, 0.76), p(0.72, 0.74)]), a: "Swing right as the checkdown.", roleName: "Swing" },
      Z: { rt: "route", route: line("Z", [p(0.86, 0.46), p(0.86, 0.20)]), a: "Outside vertical on the right.", roleName: "Go" },
    }),
  },
  {
    id: "base-curl-flat",
    cat: "BASE",
    category: "PASSING",
    name: "Curl Flat",
    type: "pass",
    tip: "Read flat defender. If she widens, hit the curl. If she sinks, take the flat now.",
    passAt: 0.38,
    passTo: "TE",
    hasMotion: false,
    motionPlayerLabel: null,
    motionType: null,
    call: passCall("Base", "Curl Flat", { X: "Curl", SL: "Flat", TE: "Curl", C: "Snap", Z: "Clear", RB: "Swing" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.14, 0.46), p(0.14, 0.52)]), a: "Push and settle on a curl.", roleName: "Curl" },
      SL: { rt: "route", route: line("SL", [p(0.22, 0.70), p(0.16, 0.71)]), a: "Fast flat route to stretch the underneath defender.", roleName: "Flat" },
      TE: { rt: "route", route: line("TE", [p(0.42, 0.50), p(0.42, 0.56)]), a: "Short curl inside the window.", roleName: "Curl" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and stay centered.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.72)]), a: "Quick drop and throw on rhythm.", roleName: "Drop" },
      RB: { rt: "route", route: line("RB", [p(0.54, 0.79), p(0.62, 0.75), p(0.70, 0.73)]), a: "Swing route away from curl side.", roleName: "Swing" },
      Z: { rt: "route", route: line("Z", [p(0.86, 0.46), p(0.86, 0.24)]), a: "Vertical clear to hold the corner deep.", roleName: "Clear" },
    }),
  },
  {
    id: "base-cross",
    cat: "BASE",
    category: "PASSING",
    name: "Cross",
    type: "pass",
    tip: "Keep the crosser moving. Throw in front and let her run after catch.",
    passAt: 0.42,
    passTo: "SL",
    hasMotion: false,
    motionPlayerLabel: null,
    motionType: null,
    call: passCall("Base", "Cross", { X: "Post", SL: "Cross", TE: "Sit", C: "Snap", Z: "Go", RB: "Check Swing" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.18, 0.48), p(0.30, 0.28)]), a: "Skinny post to occupy deep help.", roleName: "Post" },
      SL: { rt: "route", route: line("SL", [p(0.32, 0.66), p(0.46, 0.60), p(0.64, 0.60), p(0.80, 0.57)]), a: "Shallow cross under the traffic.", roleName: "Cross" },
      TE: { rt: "route", route: line("TE", [p(0.42, 0.56)]), a: "Sit over the ball.", roleName: "Sit" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Anchor after the snap.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.72)]), a: "Hold with eyes, then hit the crosser on the move.", roleName: "Drop" },
      RB: { rt: "route", route: line("RB", [p(0.55, 0.78), p(0.64, 0.74)]), a: "Check and swing right as a late outlet.", roleName: "Check Swing" },
      Z: { rt: "route", route: line("Z", [p(0.86, 0.46), p(0.86, 0.20)]), a: "Vertical clear to remove outside help.", roleName: "Go" },
    }),
  },
  {
    id: "base-trips-flood",
    cat: "BASE",
    category: "PASSING",
    name: "Trips Flood",
    type: "pass",
    tip: "Three levels on one side. High, medium, low. Read outside-in with quick feet.",
    passAt: 0.44,
    passTo: "Z",
    hasMotion: true,
    motionPlayerLabel: "RB",
    motionType: "shift",
    call: passCall("Base", "Trips Flood", { X: "Post", SL: "Flat", TE: "Corner", C: "Snap", Z: "Out", RB: "Shift Wide" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.18, 0.48), p(0.28, 0.28)]), a: "Backside post to hold the middle.", roleName: "Post" },
      SL: { rt: "route", route: line("SL", [p(0.26, 0.70), p(0.20, 0.71)]), a: "Fast flat as the low route.", roleName: "Flat" },
      TE: { rt: "route", route: line("TE", [p(0.46, 0.46), p(0.60, 0.30)]), a: "Corner route as the deep flood layer.", roleName: "Corner" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and set the point.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.72)]), a: "Read the flood: low to medium to deep.", roleName: "Drop" },
      RB: { rt: "route", route: line("RB", [p(0.68, 0.74), p(0.82, 0.70)]), mr: line("RB", [p(0.58, 0.84), p(0.66, 0.78), p(0.72, 0.74)]), a: "Shift wide before snap to create trips and identify coverage.", roleName: "Shift Wide" },
      Z: { rt: "route", route: line("Z", [p(0.74, 0.52), p(0.66, 0.52)]), a: "Quick out as the medium layer.", roleName: "Out" },
    }),
  },
  {
    id: "base-pick-slant",
    cat: "BASE",
    category: "PASSING",
    name: "Pick Slant",
    type: "pass",
    tip: "Sell space, not contact. The short sit route creates traffic without drawing a flag.",
    passAt: 0.30,
    passTo: "Z",
    hasMotion: false,
    motionPlayerLabel: null,
    motionType: null,
    call: passCall("Base", "Pick Slant", { X: "Sit", SL: "Cross", TE: "Sit", C: "Snap", Z: "Slant", RB: "Check" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.16, 0.56)]), a: "Stop in space and stay legal.", roleName: "Sit" },
      SL: { rt: "route", route: line("SL", [p(0.34, 0.66), p(0.46, 0.60)]), a: "Quick shallow route creating natural traffic.", roleName: "Cross" },
      TE: { rt: "route", route: line("TE", [p(0.42, 0.56)]), a: "Short settle route over the ball.", roleName: "Sit" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and settle.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.72)]), a: "Catch and fire fast before traffic clears.", roleName: "Quick Throw" },
      RB: { rt: "route", route: line("RB", [p(0.54, 0.80), p(0.60, 0.76)]), a: "Check and leak to the right.", roleName: "Check" },
      Z: { rt: "route", route: line("Z", [p(0.78, 0.56), p(0.66, 0.48)]), a: "Fast slant behind the traffic window.", roleName: "Slant" },
    }),
  },
  {
    id: "base-empty-flood",
    cat: "BASE",
    category: "PASSING",
    name: "Empty Flood",
    type: "pass",
    tip: "Use the shift to empty to diagnose man or zone and stretch the right side.",
    passAt: 0.42,
    passTo: "SL",
    hasMotion: true,
    motionPlayerLabel: "RB",
    motionType: "shift",
    call: passCall("Base", "Empty Flood", { X: "Hitch", SL: "Corner", TE: "Out", C: "Snap", Z: "Go", RB: "Shift Empty" }),
    players: formationPlayers("BASE", {
      X: { rt: "route", route: line("X", [p(0.14, 0.54)]), a: "Backside hitch as a fast answer.", roleName: "Hitch" },
      SL: { rt: "route", route: line("SL", [p(0.36, 0.58), p(0.50, 0.38)]), a: "Corner route into open grass.", roleName: "Corner" },
      TE: { rt: "route", route: line("TE", [p(0.50, 0.54), p(0.58, 0.54)]), a: "Short out as the intermediate layer.", roleName: "Out" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and settle in the middle.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.50, 0.72)]), a: "Work empty count and throw off leverage.", roleName: "Drop" },
      RB: { rt: "route", route: line("RB", [p(0.76, 0.72)]), mr: line("RB", [p(0.60, 0.82), p(0.68, 0.77), p(0.74, 0.72)]), a: "Shift wide pre-snap to make the defense declare.", roleName: "Shift Empty" },
      Z: { rt: "route", route: line("Z", [p(0.86, 0.46), p(0.86, 0.20)]), a: "Outside vertical clear.", roleName: "Go" },
    }),
  },
  {
    id: "boxl-jet-sweep",
    cat: "BOXL",
    category: "RUNNING",
    name: "Jet Sweep",
    type: "run",
    tip: "Jet motion must hit full speed before the snap. Everyone else should work away from the jet path.",
    passAt: null,
    passTo: null,
    hasMotion: true,
    motionPlayerLabel: "RB",
    motionType: "jet",
    call: passCall("Box Left", "Jet Sweep", { X: "Sit", SL: "Clear", TE: "Delay", C: "Snap", Z: "Drag", RB: "Jet Right" }),
    players: formationPlayers("BOXL", {
      X: { rt: "route", route: line("X", [p(0.18, 0.56)]), a: "Short sit route away from the jet direction.", roleName: "Sit" },
      SL: { rt: "route", route: line("SL", [p(0.18, 0.56), p(0.14, 0.42)]), a: "Backside clear vertically away from the run lane.", roleName: "Clear" },
      TE: { rt: "route", route: line("TE", [p(0.28, 0.56)]), a: "Delay and settle inside.", roleName: "Delay" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and stay centered.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.52, 0.74), p(0.56, 0.74)]), a: "Open right and pitch the jet path.", roleName: "Open Right" },
      RB: { rt: "run", route: line("RB", [p(0.46, 0.76), p(0.58, 0.70), p(0.66, 0.58), p(0.66, 0.38)]), mr: line("RB", [p(0.40, 0.80), p(0.48, 0.78), p(0.56, 0.76)]), a: "Jet from the bunch across the QB and turn north-south on the right.", roleName: "Jet Right" },
      Z: { rt: "route", route: line("Z", [p(0.46, 0.62), p(0.58, 0.62)]), a: "Short drag route away from the jet lane.", roleName: "Drag" },
    }),
  },
  {
    id: "boxl-fake-pass",
    cat: "BOXL",
    category: "PASSING",
    name: "Fake Pass",
    type: "pass",
    tip: "Same jet look as sweep. If defenders fly to motion, hit the slant or cross behind them.",
    passAt: 0.34,
    passTo: "Z",
    hasMotion: true,
    motionPlayerLabel: "RB",
    motionType: "jet",
    call: passCall("Box Left", "Fake Pass", { X: "Flag", SL: "Cross", TE: "Sit", C: "Snap", Z: "Slant", RB: "Jet Fake" }),
    players: formationPlayers("BOXL", {
      X: { rt: "route", route: line("X", [p(0.24, 0.50), p(0.16, 0.38)]), a: "Flag route to the corner away from motion.", roleName: "Flag" },
      SL: { rt: "route", route: line("SL", [p(0.34, 0.68), p(0.48, 0.60), p(0.62, 0.58)]), a: "Cross through the wash after the fake.", roleName: "Cross" },
      TE: { rt: "route", route: line("TE", [p(0.28, 0.56)]), a: "Sit in the first window.", roleName: "Sit" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and stay balanced.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.52, 0.74)]), a: "Show jet action, reset feet, and read flag-slant-cross.", roleName: "Ride and Throw" },
      RB: { rt: "run", route: line("RB", [p(0.48, 0.76), p(0.60, 0.72)]), mr: line("RB", [p(0.40, 0.80), p(0.48, 0.78), p(0.56, 0.76)]), a: "Flash jet motion to pull coverage, then continue to flat space.", roleName: "Jet Fake" },
      Z: { rt: "route", route: line("Z", [p(0.48, 0.62), p(0.60, 0.52)]), a: "Quick slant behind overreaction to motion.", roleName: "Slant" },
    }),
  },
  {
    id: "gun-rb-jet-left",
    cat: "GUN",
    category: "RUNNING",
    name: "RB Jet Left",
    type: "run",
    tip: "Gun look gives equal threat both ways. Hit the motion quickly and get vertical on the left.",
    passAt: null,
    passTo: null,
    hasMotion: true,
    motionPlayerLabel: "RB",
    motionType: "jet",
    call: passCall("Gun", "RB Jet Left", { X: "Clear", SL: "Out", TE: "Sit", C: "Snap", Z: "Go", RB: "Jet Left" }),
    players: formationPlayers("GUN", {
      X: { rt: "route", route: line("X", [p(0.16, 0.46), p(0.16, 0.28)]), a: "Backside clear route.", roleName: "Clear" },
      SL: { rt: "route", route: line("SL", [p(0.72, 0.68), p(0.66, 0.68)]), a: "Short out opposite the run lane.", roleName: "Out" },
      TE: { rt: "route", route: line("TE", [p(0.36, 0.56)]), a: "Short sit route inside.", roleName: "Sit" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and stay square.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.48, 0.76)]), a: "Catch and hand to the jet crossing face.", roleName: "Mesh" },
      RB: { rt: "run", route: line("RB", [p(0.54, 0.76), p(0.46, 0.74), p(0.38, 0.66), p(0.38, 0.42)]), mr: line("RB", [p(0.56, 0.76), p(0.52, 0.76), p(0.48, 0.75)]), a: "Jet across QB and turn straight up the left side of center.", roleName: "Jet Left" },
      Z: { rt: "route", route: line("Z", [p(0.66, 0.46), p(0.66, 0.26)]), a: "Vertical clear away from the run lane.", roleName: "Go" },
    }),
  },
  {
    id: "gun-rb-jet-right",
    cat: "GUN",
    category: "RUNNING",
    name: "RB Jet Right",
    type: "run",
    tip: "Same look, opposite finish. The defense should not be able to cheat because the RB starts beside the QB.",
    passAt: null,
    passTo: null,
    hasMotion: true,
    motionPlayerLabel: "RB",
    motionType: "jet",
    call: passCall("Gun", "RB Jet Right", { X: "Go", SL: "Out", TE: "Sit", C: "Snap", Z: "Clear", RB: "Jet Right" }),
    players: formationPlayers("GUN", {
      X: { rt: "route", route: line("X", [p(0.16, 0.46), p(0.16, 0.26)]), a: "Vertical clear away from the run lane.", roleName: "Go" },
      SL: { rt: "route", route: line("SL", [p(0.84, 0.68), p(0.90, 0.68)]), a: "Short out widening the support defender.", roleName: "Out" },
      TE: { rt: "route", route: line("TE", [p(0.36, 0.56)]), a: "Sit over the ball.", roleName: "Sit" },
      C: { rt: "block", route: line("C", [p(0.50, 0.58)]), a: "Snap and hold the center point.", roleName: "Snap" },
      QB: { rt: "run", route: line("QB", [p(0.52, 0.76)]), a: "Catch, ride, and hand to the right.", roleName: "Mesh" },
      RB: { rt: "run", route: line("RB", [p(0.64, 0.74), p(0.70, 0.66), p(0.70, 0.42)]), mr: line("RB", [p(0.62, 0.76), p(0.66, 0.74)]), a: "Jet to the right and get vertical right now.", roleName: "Jet Right" },
      Z: { rt: "route", route: line("Z", [p(0.66, 0.46), p(0.66, 0.28)]), a: "Clear vertically as backside spacing.", roleName: "Clear" },
    }),
  },
];

const state = {
  formation: "BASE",
  playId: "base-rb-left",
  speed: 1,
  phase: "idle",
  animation: null,
  paused: false,
  pauseAccum: 0,
  pauseStartedAt: 0,
  motionCompletion: 0,
  snapCompletion: 0,
};

const canvas = document.getElementById("fieldCanvas");
const ctx = canvas.getContext("2d");

const tabsEl = document.getElementById("formationTabs");
const runningButtonsEl = document.getElementById("runningButtons");
const passingButtonsEl = document.getElementById("passingButtons");
const playTitleEl = document.getElementById("playTitle");
const playTypeChipEl = document.getElementById("playTypeChip");
const speedChipEl = document.getElementById("speedChip");
const callLabelEl = document.getElementById("callLabel");
const callTilesEl = document.getElementById("callTiles");
const assignmentsToggleEl = document.getElementById("assignmentsToggle");
const assignmentsPanelEl = document.getElementById("assignmentsPanel");
const assignmentsListEl = document.getElementById("assignmentsList");
const coachingTipEl = document.getElementById("coachingTip");
const speedSelectEl = document.getElementById("speedSelect");

const DURATIONS = {
  motion: 900,
  pause: 200,
  snap: 2400,
};

function getPlay() {
  return PLAYS.find((p) => p.id === state.playId);
}

function getVisiblePlays() {
  return PLAYS.filter((p) => p.cat === state.formation);
}

function renderTabs() {
  tabsEl.innerHTML = "";
  Object.values(FORMATIONS).forEach((formation) => {
    const btn = document.createElement("button");
    btn.className = `formation-tab ${formation.tabClass} ${formation.id === state.formation ? "active" : ""}`;
    btn.textContent = formation.label;
    btn.onclick = () => {
      stopAnimation();
      state.formation = formation.id;
      const visible = getVisiblePlays();
      state.playId = visible[0].id;
      state.phase = "idle";
      state.motionCompletion = 0;
      state.snapCompletion = 0;
      renderUI();
      draw();
    };
    tabsEl.appendChild(btn);
  });
}

function renderPlayButtons() {
  const visible = getVisiblePlays();
  const running = visible.filter((p) => p.category === "RUNNING");
  const passing = visible.filter((p) => p.category === "PASSING");

  runningButtonsEl.innerHTML = "";
  passingButtonsEl.innerHTML = "";

  running.forEach((play) => runningButtonsEl.appendChild(makePlayButton(play)));
  passing.forEach((play) => passingButtonsEl.appendChild(makePlayButton(play)));
}

function makePlayButton(play) {
  const btn = document.createElement("button");
  btn.className = `play-btn ${play.id === state.playId ? "active" : ""}`;
  btn.textContent = play.name;
  btn.onclick = () => {
    stopAnimation();
    state.playId = play.id;
    state.phase = "idle";
    state.motionCompletion = 0;
    state.snapCompletion = 0;
    renderUI();
    draw();
  };
  return btn;
}

function parseCallTiles(call) {
  const split = call.split(" — ");
  const detail = split[1] || "";
  const items = detail.split(",").map((s) => s.trim());
  const map = {};
  items.forEach((part) => {
    const spaceIdx = part.indexOf(" ");
    const pos = part.slice(0, spaceIdx);
    map[pos] = part.slice(spaceIdx + 1);
  });
  return map;
}

function renderCallCard(play) {
  callLabelEl.textContent = play.call;
  const tiles = parseCallTiles(play.call);
  callTilesEl.innerHTML = "";
  POSITIONS.forEach((pos) => {
    const tile = document.createElement("div");
    tile.className = "call-tile";
    tile.innerHTML = `<div class="pos" style="color:${POS_COLORS[pos]}">${pos}</div><div class="name">${tiles[pos] || ""}</div>`;
    callTilesEl.appendChild(tile);
  });
}

function renderAssignments(play) {
  assignmentsListEl.innerHTML = "";
  play.players.forEach((player) => {
    const item = document.createElement("div");
    item.className = "assignment-item";
    item.innerHTML = `
      <div class="assignment-head">
        <span class="badge" style="background:${player.color}">${player.label}</span>
        <strong>${player.roleName}</strong>
      </div>
      <div class="assignment-text">${player.a}</div>
    `;
    assignmentsListEl.appendChild(item);
  });
  coachingTipEl.textContent = play.tip;
}

function renderUI() {
  const play = getPlay();
  renderTabs();
  renderPlayButtons();
  playTitleEl.textContent = `${FORMATIONS[play.cat].label} ${play.name}`;
  playTypeChipEl.textContent = play.category;
  speedChipEl.textContent = `${state.speed}x`;
  renderCallCard(play);
  renderAssignments(play);
}

assignmentsToggleEl.onclick = () => {
  const hidden = assignmentsPanelEl.classList.contains("hidden");
  assignmentsPanelEl.classList.toggle("hidden");
  assignmentsToggleEl.textContent = hidden ? "Hide Assignments" : "Show Assignments";
  assignmentsToggleEl.setAttribute("aria-expanded", hidden ? "true" : "false");
};

speedSelectEl.onchange = (e) => {
  state.speed = Number(e.target.value);
  speedChipEl.textContent = `${state.speed}x`;
};

document.getElementById("motionBtn").onclick = () => startMotionOnly();
document.getElementById("snapBtn").onclick = () => startSnapSequence();
document.getElementById("pauseBtn").onclick = () => togglePause();
document.getElementById("replayBtn").onclick = () => replay();
document.getElementById("resetBtn").onclick = () => resetPlay();

function resetPlay() {
  stopAnimation();
  state.phase = "idle";
  state.motionCompletion = 0;
  state.snapCompletion = 0;
  draw();
}

function replay() {
  stopAnimation();
  startSnapSequence();
}

function stopAnimation() {
  if (state.animation && state.animation.raf) {
    cancelAnimationFrame(state.animation.raf);
  }
  state.animation = null;
  state.paused = false;
}

function togglePause() {
  if (!state.animation) return;
  if (!state.paused) {
    state.paused = true;
    state.pauseStartedAt = performance.now();
  } else {
    state.paused = false;
    state.pauseAccum += performance.now() - state.pauseStartedAt;
    tick();
  }
}

function startMotionOnly() {
  const play = getPlay();
  stopAnimation();
  state.phase = "motion";
  state.motionCompletion = 0;
  state.snapCompletion = 0;
  state.pauseAccum = 0;
  state.animation = {
    mode: "motionOnly",
    startedAt: performance.now(),
    raf: null,
  };
  tick();
}

function startSnapSequence() {
  const play = getPlay();
  stopAnimation();
  state.phase = play.hasMotion ? "motion" : "snap";
  state.motionCompletion = 0;
  state.snapCompletion = 0;
  state.pauseAccum = 0;
  state.animation = {
    mode: "full",
    startedAt: performance.now(),
    raf: null,
  };
  tick();
}

function tick() {
  if (!state.animation || state.paused) return;
  const play = getPlay();
  const now = performance.now();
  const elapsed = (now - state.animation.startedAt - state.pauseAccum) * state.speed;

  if (state.animation.mode === "motionOnly") {
    if (play.hasMotion) {
      state.phase = "motion";
      state.motionCompletion = Math.min(1, elapsed / DURATIONS.motion);
    } else {
      state.phase = "idle";
      state.motionCompletion = 0;
    }
    draw();
    if (state.motionCompletion < 1) {
      state.animation.raf = requestAnimationFrame(tick);
    } else {
      state.animation = null;
    }
    return;
  }

  let localElapsed = elapsed;

  if (play.hasMotion) {
    if (localElapsed < DURATIONS.motion) {
      state.phase = "motion";
      state.motionCompletion = localElapsed / DURATIONS.motion;
      state.snapCompletion = 0;
      draw();
      state.animation.raf = requestAnimationFrame(tick);
      return;
    }
    state.motionCompletion = 1;
    localElapsed -= DURATIONS.motion;
    if (localElapsed < DURATIONS.pause) {
      state.phase = "pause";
      draw();
      state.animation.raf = requestAnimationFrame(tick);
      return;
    }
    localElapsed -= DURATIONS.pause;
  }

  state.phase = "snap";
  state.snapCompletion = Math.min(1, localElapsed / DURATIONS.snap);
  draw();

  if (state.snapCompletion < 1) {
    state.animation.raf = requestAnimationFrame(tick);
  } else {
    state.phase = "done";
    state.animation = null;
  }
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

function interpPoint(a, b, t) {
  return { x: lerp(a.x, b.x, t), y: lerp(a.y, b.y, t) };
}

function pointAlong(points, t) {
  if (!points || points.length === 0) return null;
  if (points.length === 1) return points[0];
  const segs = points.length - 1;
  const raw = Math.max(0, Math.min(0.999999, t)) * segs;
  const idx = Math.floor(raw);
  const local = raw - idx;
  return interpPoint(points[idx], points[idx + 1], local);
}

function getPlayerStart(player) {
  return { x: player.x, y: player.y };
}

function getMotionPath(player) {
  if (!player.mr || player.mr.length === 0) return [getPlayerStart(player)];
  return [getPlayerStart(player), ...player.mr];
}

function getRoutePath(player) {
  const motionEnd = player.mr && player.mr.length ? player.mr[player.mr.length - 1] : getPlayerStart(player);
  return [motionEnd, ...player.route];
}

function getPlayerPosition(player) {
  const start = getPlayerStart(player);
  if (state.phase === "idle") return start;

  if ((state.phase === "motion" || state.phase === "pause" || state.phase === "snap" || state.phase === "done") && player.mr && player.mr.length) {
    const motionPath = getMotionPath(player);
    const motionT = state.phase === "motion" ? state.motionCompletion : 1;
    const afterMotion = pointAlong(motionPath, motionT);
    if (state.phase === "motion" || state.phase === "pause") return afterMotion;
    const routePath = getRoutePath(player);
    return pointAlong(routePath, state.snapCompletion);
  }

  if (state.phase === "snap" || state.phase === "done") {
    const routePath = [start, ...player.route];
    return pointAlong(routePath, state.snapCompletion);
  }

  return start;
}

function scaleX(x) { return x * canvas.width; }
function scaleY(y) { return y * canvas.height; }

function drawField() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#182e18";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "rgba(255,255,255,0.08)";
  ctx.lineWidth = 1;
  for (let i = 1; i < 10; i++) {
    const x = (canvas.width / 10) * i;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }
  for (let i = 1; i < 6; i++) {
    const y = (canvas.height / 6) * i;
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }

  const losY = scaleY(0.62);
  ctx.strokeStyle = "#f0b429";
  ctx.setLineDash([10, 8]);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, losY);
  ctx.lineTo(canvas.width, losY);
  ctx.stroke();
  ctx.setLineDash([]);
}

function drawArrowHead(x1, y1, x2, y2, color) {
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const size = 8;
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - size * Math.cos(angle - Math.PI / 6), y2 - size * Math.sin(angle - Math.PI / 6));
  ctx.lineTo(x2 - size * Math.cos(angle + Math.PI / 6), y2 - size * Math.sin(angle + Math.PI / 6));
  ctx.closePath();
  ctx.fill();
}

function drawPolyline(points, color, width, alpha = 1, dashed = false, withArrow = false) {
  if (!points || points.length < 2) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  if (dashed) ctx.setLineDash([8, 6]);
  ctx.beginPath();
  ctx.moveTo(scaleX(points[0].x), scaleY(points[0].y));
  for (let i = 1; i < points.length; i++) {
    ctx.lineTo(scaleX(points[i].x), scaleY(points[i].y));
  }
  ctx.stroke();
  if (dashed) ctx.setLineDash([]);
  if (withArrow) {
    const p1 = points[points.length - 2];
    const p2 = points[points.length - 1];
    drawArrowHead(scaleX(p1.x), scaleY(p1.y), scaleX(p2.x), scaleY(p2.y), color);
  }
  ctx.restore();
}

function truncatePath(points, t) {
  if (!points || points.length < 2) return points || [];
  if (t <= 0) return [points[0]];
  if (t >= 1) return points;
  const segs = points.length - 1;
  const raw = t * segs;
  const idx = Math.floor(raw);
  const local = raw - idx;
  const out = points.slice(0, idx + 1);
  out.push(interpPoint(points[idx], points[idx + 1], local));
  return out;
}

function drawGhostRoutes(play) {
  play.players.forEach((player) => {
    const routePath = [player.mr && player.mr.length ? player.mr[player.mr.length - 1] : getPlayerStart(player), ...player.route];
    drawPolyline(routePath, ROUTE_COLORS[player.rt], 2, 0.15, player.rt === "block", false);
    if (player.mr && player.mr.length) {
      drawPolyline([getPlayerStart(player), ...player.mr], "#ef4444", 2, 0.18, true, false);
    }
  });
}

function drawTrails(play) {
  play.players.forEach((player) => {
    if (state.phase === "motion" && player.mr && player.mr.length) {
      const path = truncatePath(getMotionPath(player), state.motionCompletion);
      drawPolyline(path, "#ef4444", 3, 1, true, true);
    }
    if ((state.phase === "snap" || state.phase === "done") && player.route && player.route.length) {
      const routePath = [player.mr && player.mr.length ? player.mr[player.mr.length - 1] : getPlayerStart(player), ...player.route];
      const path = truncatePath(routePath, state.snapCompletion);
      drawPolyline(path, ROUTE_COLORS[player.rt], 3, 1, player.rt === "block", true);
    }
  });
}

function drawPassArc(play) {
  if (!play.passAt || !play.passTo) return;
  if (state.phase !== "snap" && state.phase !== "done") return;
  if (state.snapCompletion < play.passAt) return;

  const qb = play.players.find((p) => p.label === "QB");
  const target = play.players.find((p) => p.label === play.passTo);
  const start = getPlayerPosition(qb);
  const end = getPlayerPosition(target);
  const t = Math.min(1, (state.snapCompletion - play.passAt) / 0.18);

  const samples = [];
  for (let i = 0; i <= 24; i++) {
    const pct = (i / 24) * t;
    const x = lerp(start.x, end.x, pct);
    const yBase = lerp(start.y, end.y, pct);
    const arc = Math.sin(pct * Math.PI) * 0.08;
    samples.push({ x, y: yBase - arc });
  }
  drawPolyline(samples, "#ffd166", 2.5, 1, false, false);

  const last = samples[samples.length - 1];
  ctx.fillStyle = "#ffd166";
  ctx.beginPath();
  ctx.arc(scaleX(last.x), scaleY(last.y), 4, 0, Math.PI * 2);
  ctx.fill();
}

function drawMotionLabel(play) {
  if (state.phase !== "motion") return;
  if (!play.hasMotion) return;
  const player = play.players.find((p) => p.label === play.motionPlayerLabel);
  const pos = getPlayerPosition(player);
  ctx.fillStyle = "#ef4444";
  ctx.font = "bold 16px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(play.motionType.toUpperCase(), scaleX(pos.x), scaleY(pos.y) - 18);
}

function drawPlayers(play) {
  play.players.forEach((player) => {
    const pos = getPlayerPosition(player);
    const x = scaleX(pos.x);
    const y = scaleY(pos.y);
    const r = 17;

    if (player.label === "C") {
      ctx.fillStyle = "rgba(24,46,24,0.95)";
      ctx.strokeStyle = player.color;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    } else {
      ctx.fillStyle = player.color;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.fillStyle = player.label === "QB" || player.label === "RB" ? "#07111c" : "#f8fafc";
    ctx.font = "bold 12px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(player.label, x, y + 0.5);
  });
}

function draw() {
  const play = getPlay();
  drawField();
  drawGhostRoutes(play);
  drawTrails(play);
  drawPassArc(play);
  drawPlayers(play);
  drawMotionLabel(play);
}

function init() {
  renderUI();
  draw();
}

init();
