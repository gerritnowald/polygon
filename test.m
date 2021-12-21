clear
close all

%% Input

b = 2;
h = 7;
Ecken = [
    0, 0;
    b, 0;
    b, h;
    0, h;
    0, 0
    ]
A_analytic  = b*h
A2_analytic = [b*h^3, b^3*h]/12


% % Dreieck:
% a = 6;
% h = 3;
% Ecken = [
%     0, 0;
%     a, 0;
%     a/2, h;
%     0, 0
%     ];
% A_analytic  = 0.5*a*h
% A2_analytic = [a*h^3/36, a^3*h/48]

%% Berechnung

[A, yS, zS, Iy, Iz, Iyz, IyS, IzS, IyzS, phi, Ieta, Izeta] = fun_poly(Ecken);
A
[IyS, IzS]


%% plot

y_num = Ecken(:,1);
z_num = Ecken(:,2);

figure
hold on
plot(y_num,z_num, 'b')
axis equal
grid on
plot(yS, zS, 'xr')