% Written by Niamh McCann
% 2019
   
%The network will be given the opening notes to a specific piece
%This program tests the similarity between the notes of the actual piece
%and the notes of the generated piece

%This program can also test for overfitting between the generated piece and
%the training data

clear variables;
close all; 

%% 
% if testing against training data
% training = func_training();

%%
%list of all the text files from the network
mylist = ls('*.txt');
mylist = string(mylist);

overfit = zeros(13, length(mylist)); 

%% 
for num = 1:length(mylist)
    generated = dlmread(mylist(num)); %turn text file into matrix
    [overfit_2, overfit_3, overfit_4, overfit_5, overfit_6, overfit_7, overfit_8, overfit_9, overfit_10, overfit_15, overfit_20, overfit_25, overfit_30] = similarity(generated, test);
    
    overfit(1,num) = overfit_2;
    overfit(2,num) = overfit_3;
    overfit(3,num) = overfit_4;
    overfit(4,num) = overfit_5;
    overfit(5,num) = overfit_6;
    overfit(6,num) = overfit_7;
    overfit(7,num) = overfit_8;
    overfit(8,num) = overfit_9;
    overfit(9,num) = overfit_10;
    overfit(10,num) = overfit_15;
    overfit(11,num) = overfit_20;
    overfit(12,num) = overfit_25;
    overfit(13,num) = overfit_30;
end

C = [transpose(mylist) ; overfit];

%% FUNCTIONS
function [overfit_2, overfit_3, overfit_4, overfit_5, overfit_6, overfit_7, overfit_8, overfit_9, overfit_10, overfit_15, overfit_20, overfit_25, overfit_30] = similarity(generated, test_piece)
%function to test similarity between the generated piece against or the
%original piece or the training data (to test for overfitting)
%The function takes portions of various lengths of both data and compares
%them to each other, if they are equal they are added to a counter and this
%counter is returned.

    overfit_2 = 0; %iter = 2
    overfit_3 = 0;
    overfit_4 = 0;
    overfit_5 = 0;
    overfit_6 = 0;
    overfit_7 = 0;
    overfit_8 = 0;
    overfit_9 = 0;
    overfit_10 = 0;
    overfit_15 = 0; %iter = 11
    overfit_20 = 0;
    overfit_25 = 0;
    overfit_30 = 0; %iter = 14

    for iter = 2:14 %iter
        for a = 1:length(test_piece) %test_piece = training data if testing for overfitting
            if (iter == 2)
                n = 2;
                section_test = test_piece(a:a+1,:);
            elseif (iter == 3)
                n = 3;
                section_test = test_piece(a:a+2,:);
            elseif (iter == 4)
                n = 4;
                section_test = test_piece(a:a+3,:);
            elseif (iter == 5)
                n = 5;
                section_test = test_piece(a:a+4,:);
            elseif (iter == 6)
                n = 6;
                section_test = test_piece(a:a+5,:);
            elseif (iter == 7)
                n = 7;
                section_test = test_piece(a:a+6,:);
            elseif (iter == 8)
                n = 8;
                section_test = test_piece(a:a+7,:);
            elseif (iter ==9)
                n = 9;
                section_test = test_piece(a:a+8,:);
            elseif (iter == 10)
                n = 10;
                section_test = test_piece(a:a+9,:);
            elseif (iter == 11) %chunk of 15
                n = 15;
                section_test = test_piece(a:a+14,:);
            elseif (iter == 12) %chunk of 20
                n = 20;
                section_test = test_piece(a:a+19,:);
            elseif (iter == 13) %chunk of 25
                n = 25;
                section_test = test_piece(a:a+24,:);
            else %chunk of 30
                n = 30;
                section_test = test_piece(a:a+29,:);
            end

            if (a == length(test_piece) - n)
                break;
            end

            for b = 1:length(generated)
                if (iter == 2)
                    section_gen = generated(b:b+1,:);
                elseif (iter == 3)
                    section_gen = generated(b:b+2,:);
                elseif (iter == 4)
                    section_gen = generated(b:b+3,:);
                elseif (iter == 5)
                    section_gen = generated(b:b+4,:);
                elseif (iter == 6)
                    section_gen = generated(b:b+5,:);
                elseif (iter == 7)
                    section_gen = generated(b:b+6,:);
                elseif (iter == 8)
                    section_gen = generated(b:b+7,:);
                elseif (iter == 9)
                    section_gen = generated(b:b+8,:);
                elseif (iter == 10)
                    section_gen = generated(b:b+9,:);
                elseif (iter == 11) %chunk of 15
                    section_gen = generated(b:b+14,:);
                elseif (iter == 12) %chunk of 20
                    section_gen = generated(b:b+19,:);
                elseif (iter == 13) %chunk of 25
                    section_gen = generated(b:b+24,:);
                else %chunk of 30
                    section_gen = generated(b:b+29,:);
                end

                if (b == length(generated) - n)
                    break;
                end

                if (section_gen == section_test)
                    if (iter == 2)
                        overfit_2 = overfit_2 + 1;
                    elseif (iter == 3)
                        overfit_3 = overfit_3 + 1;
                    elseif (iter == 4)
                        overfit_4 = overfit_4 + 1;
                    elseif (iter == 5)
                        overfit_5 = overfit_5 + 1;
                    elseif (iter == 6)
                        overfit_6 = overfit_6 + 1;
                    elseif (iter == 7)
                        overfit_7 = overfit_7 + 1;
                    elseif (iter == 8)
                        overfit_8 = overfit_8 + 1;
                    elseif (iter == 9)
                        overfit_9 = overfit_9 + 1;
                    elseif (iter == 10)
                        overfit_10 = overfit_10 + 1;
                    elseif (iter == 11)
                        overfit_15 = overfit_15 + 1;
                    elseif (iter == 12)
                        overfit_20 = overfit_20 + 1;
                    elseif (iter == 13)
                        overfit_25 = overfit_25 + 1;
                    else 
                        overfit_30 = overfit_30 + 1;
                    end
                end
            end
        end
    end
end

function training = func_training()
    %if needed change directory to where the training data is kept
    %cd 
    training = textread('training_off.txt','%s', 'endofline', '\n', 'delimiter', ' ');
    [row, ~] = size(training);
    training = str2double(training);
    training2 = zeros(1,1);

     for b = 1:row
         if isnan(training(b)) 
             %if not a number, i.e, ignore S and E flags 
             %as these won't be in generated files
             continue
         else
             training2(end+1,1) = training(b);          
         end
     end
    training2 = training2(2:end,:);
    
    training = zeros(1,3);
    [row, ~] = size(training2);
    for c = 1:3:row
        training(end+1,1) = training2(c);
        training(end,2) = training2(c+1);
        training(end,3) = training2(c+2);
    end
    training = training(2:end, :);
    clear training2
    
    % return to previous directory
    % cd 
end