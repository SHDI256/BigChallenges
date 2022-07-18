service DataTransfer {
    void data_transfer_image(1:binary img)
    void data_transfer_int(1:list <i16> data),
    void data_transfer_bool(1:list <bool> data),
    binary request_image_transfer(),
    list <double> request_data_transfer_double(),
    void request_predict_transfer(1:i16 predict),
    void data_transfer_verdict(1:bool verdict)
}

service DataRegistration {
    void data_transfer_photo(1:binary img),
    void data_transfer_full_name(1:list <string> full_name),
    void data_transfer_sex(1:bool sex),
    void data_transfer_age(1:i16 age),

    void data_transfer_int(1:list <i16> data),
    void data_transfer_double(1:list <double> data)
}