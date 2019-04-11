cd C:\Users\Niamh\Desktop\College\5th_year\Thesis\DataBase_T\JSB_Chorales_T\val_T

% Functions have been used from the following source
% https://github.com/miditoolbox/1.1
   
%Program to create the training, validation and testing data for the neural network. 

clear variables;
close all; 

%%
%create a list of all MIDI files in the folder
mylist = ls('*.mid');
mylist = string(mylist);

%dur encoding: 1: Onset, 2: Duration, 3: MIDI note number
%off encoding: 1: Onset, 2: Offset, 3: MIDI note number

for num = 1:length(mylist)
    [nmat, midi] = readmidi_mtb(mylist(num));
    
    nmat_dur(:,1) = round(nmat(:,1));
    nmat_off(:,1) = round(nmat(:,1));
    
    off  = round(nmat(:,1)) + round(nmat(:,2));
    nmat_dur(:,2) = round(nmat(:,2));
    nmat_off(:,2) = off;
    
    nmat_dur(:,3) = round(nmat(:,4));
    nmat_off(:,3) = round(nmat(:,4));
    
    if num == 1 %if first in list start a new file
       export(nmat_dur, 0, 'training_dur');
       export(nmat_off, 0, 'training_off');
    else %else append to file
       export(nmat_dur, 1, 'training_dur');
       export(nmat_off, 1, 'training_off');
    end
    
    clear nmat_dur
    clear nmat_off
end

%% FUNCTION
function export(nmat, n, filename)
%exporting to text file
    format_name = '%s.txt';
    text_name = sprintf(format_name, filename);
    formatSpec = '%d %d %d \r\n';
    flag_format = '%s \r\n'; %Flag format will be one character
    [nrows, ~] = size(nmat);
       
    if n == 0 
        fileID = fopen(text_name, 'w');
        fprintf(fileID, flag_format, 'S');
        [nrows, ncols] = size(nmat);
        for row = 1:nrows
            fprintf(fileID, formatSpec, nmat(row,:));
        end
    end

    if n ==1 
        fileID = fopen(text_name, 'a');
        fprintf(fileID, flag_format, 'S');
        for row = 1:nrows
            fprintf(fileID, formatSpec, nmat(row,:));
        end
    end
    
    fprintf(fileID, flag_format, 'E');
    fclose(fileID);
end

