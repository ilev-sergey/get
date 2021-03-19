%% Изучение красного смещения звёзд

close all
clear variables
%% Импорт данных

spectra = importdata("spectra.csv"); % измерения
starNames = importdata("star_names.csv");
lambdaStart = importdata("lambda_start.csv");
lambdaDelta = importdata("lambda_delta.csv");
%% Константы

speedOfLight = 299792.458; % км/c
lambdaPr = 656.28; % нм
%% Предварительная обработка данных

starAmount = length(starNames);
spectraSize = size(spectra);
spectraAmount = spectraSize(1);
intensity = zeros(1, starAmount); index = zeros(1, starAmount); speed = zeros(1, starAmount);
%% Определение диапазона длин волн

lambda = (lambdaStart : lambdaDelta : lambdaStart + (spectraAmount-1) * lambdaDelta)';
%% Расчёты и построение графика

for i = (1 : starAmount)
    min(spectra)
    [intensity(1, i), index(1, i)] = min(spectra(:, i)); % определение минимальных интенсивностей и их индексов
    z = lambda(index(1,i)) / lambdaPr - 1; % определение смещения
    speed(1, i) = z * speedOfLight; % определение скорости
    % Построение графика
   if z >= 0
        plot(lambda, spectra(:, i), '-', 'LineWidth', 3)
    else
        plot(lambda, spectra(:, i), '--', 'LineWidth', 1)
   end
   hold on
end
set(gcf, 'Visible', 'on')
xlabel('Длина волны, нм')
ylabel(['Интенсивность, эрг./см^2/с/', char(197)])
title('Спектры звёзд')
text(min(lambda)+(max(lambda)-min(lambda))*0.1, max(max(spectra))* 1.05, 'Сергей Ильев, Б04-004')
grid on
legend(starNames)
hold off
speed = speed';
%% Удаляющиеся от Земли звёзды

movaway = starNames(speed > 0);
%% Сохранение графика

saveas(gcf, 'spectra.png')