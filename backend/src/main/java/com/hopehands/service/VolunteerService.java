package com.hopehands.service;

import com.hopehands.dto.RoleCount;
import com.hopehands.model.Volunteer;
import com.hopehands.repository.VolunteerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class VolunteerService {

    @Autowired
    private VolunteerRepository volunteerRepository;

    public Volunteer createVolunteer(Volunteer volunteer) {
        volunteer.setStatus("pending");
        return volunteerRepository.save(volunteer);
    }

    public List<Volunteer> getVolunteers() {
        return volunteerRepository.findAll();
    }

    public Optional<Volunteer> updateVolunteer(Long id, Volunteer volunteerDetails) {
        return volunteerRepository.findById(id).map(volunteer -> {
            volunteer.setFirstName(volunteerDetails.getFirstName());
            volunteer.setLastName(volunteerDetails.getLastName());
            volunteer.setEmail(volunteerDetails.getEmail());
            volunteer.setPhoneNumber(volunteerDetails.getPhoneNumber());
            volunteer.setPreferredVolunteerRole(volunteerDetails.getPreferredVolunteerRole());
            volunteer.setAvailability(volunteerDetails.getAvailability());
            volunteer.setHowDidYouHearAboutUs(volunteerDetails.getHowDidYouHearAboutUs());
            return volunteerRepository.save(volunteer);
        });
    }

    public boolean deleteVolunteer(Long id) {
        return volunteerRepository.findById(id).map(volunteer -> {
            volunteerRepository.delete(volunteer);
            return true;
        }).orElse(false);
    }

    public Optional<Volunteer> approveVolunteer(Long id) {
        return volunteerRepository.findById(id).map(volunteer -> {
            volunteer.setStatus("approved");
            return volunteerRepository.save(volunteer);
        });
    }

    public Optional<Volunteer> rejectVolunteer(Long id) {
        return volunteerRepository.findById(id).map(volunteer -> {
            volunteer.setStatus("rejected");
            return volunteerRepository.save(volunteer);
        });
    }

    public List<RoleCount> getRoleCounts() {
        return volunteerRepository.countByPreferredVolunteerRole();
    }

    public void uploadCsv(MultipartFile file) throws IOException {
        List<Volunteer> volunteers = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(file.getInputStream()))) {
            String line;
            // Skip header
            reader.readLine();
            while ((line = reader.readLine()) != null) {
                String[] data = line.split(",");
                Volunteer volunteer = new Volunteer();
                volunteer.setFirstName(data[0]);
                volunteer.setLastName(data[1]);
                volunteer.setEmail(data[2]);
                volunteer.setPhoneNumber(data[3]);
                volunteer.setPreferredVolunteerRole(data[4]);
                volunteer.setAvailability(data[5]);
                volunteer.setHowDidYouHearAboutUs(data[6]);
                volunteer.setStatus("approved");
                volunteers.add(volunteer);
            }
        }
        volunteerRepository.saveAll(volunteers);
    }
}
