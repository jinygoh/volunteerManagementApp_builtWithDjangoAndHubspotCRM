package com.hopehands.controller;

import com.hopehands.dto.RoleCount;
import com.hopehands.model.Volunteer;
import com.hopehands.service.VolunteerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api")
public class VolunteerController {

    @Autowired
    private VolunteerService volunteerService;

    @PostMapping("/signup")
    public ResponseEntity<Volunteer> signup(@RequestBody Volunteer volunteer) {
        Volunteer createdVolunteer = volunteerService.createVolunteer(volunteer);
        return new ResponseEntity<>(createdVolunteer, HttpStatus.CREATED);
    }

    @GetMapping("/volunteers")
    public List<Volunteer> getVolunteers() {
        return volunteerService.getVolunteers();
    }

    @PutMapping("/volunteers/{id}")
    public ResponseEntity<Volunteer> updateVolunteer(@PathVariable Long id, @RequestBody Volunteer volunteerDetails) {
        return volunteerService.updateVolunteer(id, volunteerDetails)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/volunteers/{id}")
    public ResponseEntity<Void> deleteVolunteer(@PathVariable Long id) {
        return volunteerService.deleteVolunteer(id)
                ? ResponseEntity.noContent().build()
                : ResponseEntity.notFound().build();
    }

    @PostMapping("/volunteers/{id}/approve")
    public ResponseEntity<Volunteer> approveVolunteer(@PathVariable Long id) {
        return volunteerService.approveVolunteer(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/volunteers/{id}/reject")
    public ResponseEntity<Volunteer> rejectVolunteer(@PathVariable Long id) {
        return volunteerService.rejectVolunteer(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/visualizations/volunteer-roles")
    public List<RoleCount> getRoleCounts() {
        return volunteerService.getRoleCounts();
    }

    @PostMapping("/upload-csv")
    public ResponseEntity<String> uploadCsv(@RequestParam("file") MultipartFile file) {
        try {
            volunteerService.uploadCsv(file);
            return ResponseEntity.ok("CSV uploaded successfully");
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to upload CSV");
        }
    }
}
