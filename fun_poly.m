function [A, yS, zS, Iy, Iz, Iyz, IyS, IzS, IyzS, phi, Ieta, Izeta] = fun_poly(Ecken)
%% TM1 P03: Schwerpunkt und FTM über Polygonzug-/Eckenformel, zentrale und Haupt-FTM
% Autor: KB
% Datum: 29.04.19
% 
% Aufruf:    [A, yS, zS, Iy, Iz, Iyz, IyS, IzS, IyzS, phi, Ieta, Izeta] = SPEckenformel(Ecken)
% Eingangsparameter: Ecken ... Matrix der Eck-Koordinaten,
%                              Spalte 1 = x-Werte,
%                              Spalte 2 = y-Werte
% Ausgabedaten:      A     ... Flächeninhalt
%                    yS    ... Schwerpunkt (SP) y-Koordinate
%                    zS    ... Schwerpunkt z-Koordinate
%                    Iy    ... FTM bzgl. y-Koordinatenachse
%                    Iz    ... FTM bzgl. z-Koordinatenachse
%                    Iyz   ... Deviations-FTM bzgl. Koordinatenachsen
%                    IyS   ... zentrales FTM bzgl. SP-Achse || y
%                    IzS   ... zentrales FTM bzgl. SP-Achse || z
%                    IyzS  ... zentrales Deviations-FTM bzgl. SP-Achsen || y,z
%                    phi   ... Hauptachsenrichtung
%                    Ieta  ... Haupt-FTM
%                    Izeta ... Haupt-FTM, Indes 1 und 2 nach Auswertung mit
%                              Zahlenwerten festlegen (außerhalb der Funktion)
%
% ------------------------------------------------------------

%% Vorbereitung:
% x- und y-Koordinaten der Ecken:
y = Ecken(:,1);
z = Ecken(:,2);

% Anzahl der Ecken
n = length(y)-1;         % End-Ecke doppelt --> -1

%% Schwerpunkt mit Polygonzugformel:

% Initialisierung:
A   = 0;
Sy  = 0;
Sz  = 0;
Iy  = 0;
Iz  = 0;
Iyz = 0;

% Schleife für Summation:
for k = 1:n
    A   = A  + (y(k)*z(k+1) - y(k+1)*z(k)) ; % Faktor 1/2 global nach Aufsummierung
    Sy  = Sy + (y(k)*z(k+1) - y(k+1)*z(k))*(z(k)+z(k+1)); 
    Sz  = Sz + (y(k)*z(k+1) - y(k+1)*z(k))*(y(k)+y(k+1));
    Iy  = Iy  + (y(k)*z(k+1) - y(k+1)*z(k)) * ((z(k) + z(k+1))^2 - z(k) * z(k+1));     
    Iz  = Iz  + (y(k)*z(k+1) - y(k+1)*z(k)) * ((y(k) + y(k+1))^2 - y(k) * y(k+1));     
    Iyz = Iyz + (y(k)*z(k+1) - y(k+1)*z(k)) * ((y(k) + y(k+1)) * ...
            (z(k) + z(k+1)) - 1/2 * (y(k) * z(k+1) + y(k+1) * z(k))); 
end

% Vor-Faktoren berücksichtigen:
A   = A/2;       % Faktor 1/2 global nach Aufsummierung
yS  = Sz/6/A;    % Berechnung Schwerpunktkoordinate aus Stat. Moment: /A
zS  = Sy/6/A;
Iy  =  1/12 * Iy;
Iz  =  1/12 * Iz;
Iyz = -1/12 * Iyz;

% zentrale FTM:
IyS  = Iy  - zS^2 * A;
IzS  = Iz  - yS^2 * A;
IyzS = Iyz + yS * zS * A;

% Haupt-FTM:
if IyS-IzS == 0
    phi = pi/4;
else
    phi = atan((2 * IyzS)/(IyS - IzS))/2;
end

% Koordinatentransformation auf Hauptrichtung:
Ieta  = 1/2 * (IyS + IzS) + 1/2 * (IyS - IzS) * cos(2 * phi) + IyzS * sin(2 * phi);
Izeta = 1/2 * (IyS + IzS) - 1/2 * (IyS - IzS) * cos(2 * phi) - IyzS * sin(2 * phi);

% I_1 = max(I_eta, I_xi);     % hier Auswahl des Max/Min nötig, da phi nur mit atan 
% I_2 = min(I_eta, I_xi);     % noch nicht die positive Orientierung der Achse enthält

